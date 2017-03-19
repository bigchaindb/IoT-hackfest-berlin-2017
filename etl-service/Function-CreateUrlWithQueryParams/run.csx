/* 
DESCRIPTION

This function extracts the HTTP body payload (JSON) and passes this payload as query
string parameters to a newly created URL string.

Since the TomTom data serivce does only accept query string parameters this step was necessary.
However, the account credentials (username, password, apikey, etc) has to be provided - 
this implementation does only provide placeholders (<<ENDPOINT_ACCOUNT_NAME>>, 
<<ENDPOINT_USERNAME>>, <<ENDPOINT_PASSWORD>>, <<ENDPOINT_APIKEY>>)
*/


#r "Newtonsoft.Json"

using System.Net;
using Newtonsoft.Json;

public static async Task<HttpResponseMessage> Run(HttpRequestMessage req, TraceWriter log)
{
    log.Info("C# HTTP trigger function processed a request.");

    string result = "";

    // create the query URL
    // start with the mandatory parameters first
    foreach(var p in MandatoryQueryParameters)
    {
        result += string.Format("&{0}={1}", p.Key, p.Value);
    }

    // now add the optional/action specific parameters
    dynamic body = await req.Content.ReadAsStringAsync();
    var optionalQueryParams = JsonConvert.DeserializeObject<QueryParam[]>(body as string);

    foreach(var qp in optionalQueryParams)
    {
        result += string.Format("&{0}={1}", qp.Key, qp.Value);
    }

    return req.CreateResponse(HttpStatusCode.OK, result);
}

private static IDictionary<string, string> MandatoryQueryParameters {
    get 
    { 
        return new Dictionary<string, string>
            {
                { "account", "<<ENDPOINT_ACCOUNT_NAME>>" },
                { "username", "<<ENDPOINT_USERNAME>>" },
                { "password", "<<ENDPOINT_PASSWORD>>"},
                { "apikey", "<<ENDPOINT_APIKEY>>" },

            };
    }
}

public class QueryParam
{
    public string Key {get;set;}
    public string Value {get;set;}
}