from flask import Flask, json
import JumpingSpider

api = Flask(__name__)
spider = JumpingSpider.JumpingSpider()

@api.route('/spider', methods=['GET'])
def get_companies():
  return spider.go()

if __name__ == '__main__':
    api.run()

