
import db

import secrets

import time

def get_all_tasks():
        while True:
                print(db.get_tasks())
                time.sleep(10)



if __name__ == '__main__':
        print(get_all_tasks())