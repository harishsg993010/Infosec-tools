import java.io.IOException;
import java.net.InetAddress;
import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import burp.IBurpExtender;
import burp.IExtensionHelpers;
import burp.IHttpListener;
import burp.IHttpRequestResponse;

public class BurpExtender implements IBurpExtender, IHttpListener {

    private IExtensionHelpers helpers;
    private List<String> ipAddresses;
    private int currentIndex;

    @Override
    public void registerExtenderCallbacks(IBurpExtenderCallbacks callbacks) {
        // set up extension
        helpers = callbacks.getHelpers();
        callbacks.registerHttpListener(this);

        // get list of IP addresses from Heroku
        ipAddresses = new ArrayList<>();
        try {
            String response = helpers.makeHttpRequest("api.heroku.com", 443, true,
                "GET", "/apps/<YOUR_APP_NAME>/dynos", null, null);
            JSONArray dynos = new JSONObject(response).getJSONArray("dynos");
            for (int i = 0; i < dynos.length(); i++) {
                String ipAddress = dynos.getJSONObject(i).getString("public_ip");
                ipAddresses.add(ipAddress);
            }
        } catch (IOException | JSONException e) {
            e.printStackTrace();
            return;
        }

        // start at the first IP address
        currentIndex = 0;
    }

    @Override
    public void processHttpMessage(int toolFlag, boolean messageIsRequest,
        IHttpRequestResponse messageInfo) {

        // only process requests
        if (!messageIsRequest) {
            return;
        }

        // get the request message
        byte[] request = messageInfo.getRequest();

        // update the Host header with the current IP address
        List<String> headers = helpers.analyzeRequest(request).getHeaders();
        for (int i = 0; i < headers.size(); i++) {
            if (headers.get(i).startsWith("Host:")) {
                headers.set(i, "Host: " + ipAddresses.get(currentIndex));
                break;
            }
        }

        // update the request message with the new headers
        request = helpers.buildHttpMessage(headers, null);
        messageInfo.setRequest(request);

        // move to the next IP address
        currentIndex = (currentIndex + 1) % ipAddresses.size();
    }

}
