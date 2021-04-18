from flask import Flask, request, Response

app = Flask("Kek")

@app.route('/webhook', methods=['POST'])
async def respond():
    print(request.json);
    return Response(status=200)
app.run(host="0.0.0.0", port=80)
