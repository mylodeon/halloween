from flask import Flask, json
import JumpingSpider

api = Flask(__name__)
spider = JumpingSpider.JumpingSpider()

@api.route('/spider', methods=['GET'])
def get_companies():
  print "running"
  return spider.go()

@api.route('/health', methods=['GET'])
def get_health():
  return spider.instance()

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8080, debug=True, threaded=false)

