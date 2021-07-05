import pymysql

class in_mysql():
    def __init__(self,case_id_and_model):
        self.case_id_and_model = case_id_and_model
        print(type(case_id_and_model))
        self.db  = pymysql.connect("localhost", "root", "123456", "balf")
        self.cursor = self.db.cursor()
        self.sql = "DROP TABLE IF EXISTS DATABASE%s" % (self.case_id_and_model)
        self.cursor.execute(self.sql)
        self.sql = "CREATE TABLE DATABASE%s (IMG_NAME  CHAR(20) NOT NULL,CONFIDENCE FLOAT,MODEL CHAR(20) )" % (case_id_and_model)
        self.cursor.execute(self.sql)
        print('创建数据库',case_id_and_model,'成功')


    def write_in_database(self,nxn_img_name,conf,used_model):
        self.sql =  "INSERT INTO DATABASE%s(IMG_NAME,CONFIDENCE,MODEL) VALUES ('%s', %s, '%s')" %(self.case_id_and_model,nxn_img_name,conf,used_model)
        self.cursor.execute(self.sql)



def out_mysql(case_id_and_model):
    db = pymysql.connect("localhost", "root", "123456", "balf")
    cursor = db.cursor(cursor = pymysql.cursors.DictCursor) #变成字典形式的输出
    sql = "SELECT CONFIDENCE '图像块可疑度',IMG_NAME 'nxn' ,MODEL '使用的目标检测模型' FROM DATABASE%s ORDER BY CONFIDENCE DESC" % (case_id_and_model)
    cursor.execute(sql)
    results = cursor.fetchall()
    sql = "SELECT count(*) count_star FROM DATABASE%s" % (case_id_and_model)
    cursor.execute(sql)
    count_star = cursor.fetchall()
    # print(results)
    # print(count_star)
    return results,count_star



