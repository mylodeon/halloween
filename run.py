from flask import Flask, json
import JumpingSpider

api = Flask(__name__)
spider = JumpingSpider.JumpingSpider()

@api.route('/spider', methods=['GET'])
def startSpider():
  return spider.start()

@api.route('/spider-stop', methods=['GET'])
def stopSpider():
  return spider.stop()

@api.route('/health', methods=['GET'])
def get_health():
  return "healthy"

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8080, debug=False, threaded=True)

