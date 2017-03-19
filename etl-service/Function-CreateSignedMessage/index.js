var crypto = require('crypto');
var bs58 = require('bs58');

function createKey(id) {
    return bs58.encode(crypto.createHash('sha256').update(id).digest());
}

module.exports = function (context, req) {
    context.log('JavaScript HTTP trigger function processed a request.');

    var id = req.query.id || req.headers.id;
    var msgType = req.query.msgtype || req.headers.msgtype;
    var payload = req.body;

    if (id && msgType) {

        var result = payload.map(function(item) {
            var t = {}
            t.msgType = msgType;
            t.payload = item;
            t.vehicleId = createKey(id);
            return t;
        });

        res = {
            // status: 200, /* Defaults to 200 */
            body: result
        };
    }
    else {
        res = {
            status: 400,
            body: "Please pass a id on the query string or in the request body"
        };
    }
    context.done(null, res);
};