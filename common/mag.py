# -*-coding:utf-8-*-
import sys
sys.path.append('..')

from common import mysql_connector as my_con

# MAG : Manga（漫画）、Anime（アニメ）、Game（ゲーム）といったジャンルを総称する語。
# title / media / media_story / image の状態を持つクラス。
class Mag:

    def __init__(self):
        self._mag_id = None
        self._mag_name = None
        self._mag_type = None
        self._mag_dir = None
        self._mag_env = None

    @property
    def mag_id(self):
        return self._mag_id

    @mag_id.setter
    def mag_id(self,mag_id):
        self._mag_id = mag_id

    @property
    def mag_name(self):
        return self._mag_name

    @mag_id.setter
    def mag_name(self,mag_name):
        self._mag_name = mag_name

    @property
    def mag_type(self):
        return self._mag_type

    @mag_type.setter
    def mag_type(self,mag_type):
        self._mag_type = mag_type

    @property
    def mag_dir(self):
        return self._mag_dir

    @mag_dir.setter
    def mag_dir(self,mag_dir):
        self._mag_dir = mag_dir

    @property
    def mag_env(self):
        return self._mag_env

    @mag_env.setter
    def mag_env(self,mag_env):
        self._mag_env = mag_env

    def get_mag_info_from_(self,dir_path,env):
        self._mag_env = env
        self._mag_dir = dir_path.split('/')[-1]
        mag_dir_splited = self._mag_dir.split('_')
        self._mag_id = int(mag_dir_splited[0])
        # iamgesディレクトリ以下、1階層目=title / 2階層目=media / 3階層目=media_story / 4階層目=image
        dir_tree = dir_path.split("images")[1].split("/")
        if len(dir_tree) == 2:
            self._mag_type = 'title'
            self._mag_name = mag_dir_splited[1]
        elif len(dir_tree) == 3:
            self._mag_type = 'media'
            self._mag_name = mag_dir_splited[1]
        elif len(dir_tree) == 4:
            self._mag_type = 'media_story'
            upper_dir = dir_path.split('/')[-2]
            media_id = upper_dir.split('_')[0]
            self._mag_id = mag_dir_splited[0] + "," + media_id
        else:
            print(f"画像ディレクトリより下層に謎のディレクトリが存在します。")

        print(f"mag_objに 'mag_id:{self._mag_id}' , mag_type:'{self._mag_type}' , mag_name:'{self._mag_name}' , mag_directory:'{self._mag_dir}' が記録されました。")


    def has_mysql(self,dir_path):
        target_table = f"{self._mag_type}"
        # media_storyの場合のみstory_idとmedia_idをごにょごにょする必要があるので別処理。
        if self._mag_type == "media_story":
            dir_path_splited = dir_path.split('/')
            story_id = int(dir_path_splited[-1].split('_')[0])
            media_id = int(dir_path_splited[-2].split('_')[0])
            mag_id = my_con.execute_select_one(f"select concat(media_id,',',story_id) from {target_table} where media_id = {media_id} and story_id = {story_id};",self._mag_env)
        else:
            mag_id = my_con.execute_select_one(f"select {target_table}_id from {target_table} where {target_table}_name = '{self._mag_name}';",self._mag_env)
        if mag_id == None:
            print(f"<error>{self._mag_dir}のファイル名からmysqlの{self._mag_type}_idを取得できませんでした。\nマスタ情報が未登録です。")
            return False
        elif mag_id[0] != self._mag_id:
            print(f"<error>{self._mag_dir}のファイル名から取得できた{self._mag_type}_id（={self._mag_id}）とmysqlから取得できた{self._mag_type}_id（={mag_id[0]}）が一致しませんでした。")
            print(f"マスタ情報が不正の可能性があります。")
            return False
        else:
            return True


    def insert_keyword(self,dir_path,file_name):
        if self.has_mysql(dir_path):
            target_table = f"relay_{self._mag_type}_keyword"
            insert_sql = ""
            for row in open(dir_path +  "/" + file_name,"r"):
                keyword_str = row.replace('\n','')
                keyword_id = my_con.execute_select_one(f"select keyword_id from keyword where keyword_character = '{keyword_str}';",self._mag_env)
                # 既存のkeywordの登録があれば、そのkeyword_idを利用する。
                if keyword_id != None:
                    insert_sql = insert_sql \
                    + f"insert ignore into {target_table} values ({self._mag_id},{keyword_id[0]},now());\n"
                # ない場合は、keywordを新規insertする。
                else:
                    insert_sql = insert_sql \
                    + f"insert ignore into keyword (keyword_character,update_time,create_time) values ('{keyword_str}',now(),now());\n" \
                    + f"insert ignore into {target_table} values ({self._mag_id},macro_last_insert_id,now());\n"

            print(insert_sql)
            my_con.insert_query_statement(insert_sql,self._mag_env)


    def insert_mediastory_keyword(self,dir_path,file_name):
        insert_sql = ""
        if not self.has_mysql(dir_path):
            insert_sql = insert_sql \
            + f"insert ignore into media_story (media_id,story_id,create_time) values ({self._mag_id},now());\n"
        target_table = f"relay_{self._mag_type}_keyword"
        for row in open(dir_path +  "/" + file_name,"r"):
            keyword_str = row.replace('\n','')
            keyword_id = my_con.execute_select_one(f"select keyword_id from keyword where keyword_character = '{keyword_str}';",self._mag_env)
            # 既存のkeywordの登録があれば、そのkeyword_idを利用する。
            if keyword_id != None:
                insert_sql = insert_sql \
                + f"insert ignore into {target_table} values ({self._mag_id},{keyword_id[0]},now());\n"
            # ない場合は、keywordを新規insertする。
            else:
                insert_sql = insert_sql \
                + f"insert ignore into keyword (keyword_character,update_time,create_time) values ('{keyword_str}',now(),now());\n" \
                + f"insert ignore into {target_table} values ({self._mag_id},macro_last_insert_id,now());\n"
        print(insert_sql)
        my_con.insert_query_statement(insert_sql,self._mag_env)


    def insert_image_keyword(self,dir_path,file_name):
        if self.has_mysql(dir_path):
            insert_sql = ""
            for row in open(dir_path +  "/" + file_name,"r"):
                row = row.replace('\n','')
                columns = row.split(',')
                image_file_name = columns[0]
                image_id = my_con.execute_select_one(f"select image_id from image where image_name like '%{image_file_name}';",self._mag_env)
                # image既存チェック→既存のimageがあればinsertしない
                if image_id == None:
                    # image_idが取得できない場合、次の処理でimage_idを利用するため、先にinsertしておく
                    image_path = "images" + dir_path.split("images")[1] + "/" + image_file_name
                    insert_image_sql = f"insert ignore into image (image_name,create_time) values ('{image_path}',now());\n"
                    my_con.insert_query(insert_image_sql,self._mag_env)
                    image_id = my_con.execute_select_one(f"select image_id from image where image_name like '%{image_file_name}';",self._mag_env)
                # columns[0](=画像名)でimage_id を取得（上の処理でimageのinsertをしているのでimage_idが取得できないケースは無い想定。）
                for column in columns:
                    # columns[0]=画像名なので処理スキップ
                    if column != columns[0]:
                        # columns[1以降]が画像に紐づくキーワード
                        keyword_id = my_con.execute_select_one(f"select keyword_id from keyword where keyword_character = '{column}';",self._mag_env)
                        keyword_str = column
                        # keyword_idを取得できた場合
                        if keyword_id != None:
                            insert_sql = insert_sql \
                            + f"insert ignore into relay_image_keyword values ({image_id[0]},{keyword_id[0]},now()); \n"
                        # keyword_idを取得できない場合（＝# keywordの新規insertの場合）
                        else:
                            insert_sql = insert_sql \
                            + f"insert ignore into keyword (keyword_character,update_time,create_time) values ('{keyword_str}',now(),now());\n" \
                            + f"insert ignore into relay_image_keyword values ({image_id[0]},macro_last_insert_id,now()); \n"
            print(insert_sql)
            my_con.insert_query_statement(insert_sql,self._mag_env)
