import re

from burp import IBurpExtender
from burp import IScannerCheck
from burp import IScanIssue

class BurpExtender(IBurpExtender, IScannerCheck):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.registerScannerCheck(self)

        return
    def doPassiveScan(self, baseRequestResponse):
    # search for common RCE and command injection patterns in response
        response = baseRequestResponse.getResponse()
        response_str = self._helpers.bytesToString(response)
        rce_pattern = re.compile("(system\(|exec\(|popen\()")
        cmd_pattern = re.compile("(cmd.exe|/bin/bash)")

        if rce_pattern.search(response_str) or cmd_pattern.search(response_str):
            return [CustomScanIssue(baseRequestResponse.getHttpService(), self._helpers.analyzeRequest(baseRequestResponse).getUrl(), [baseRequestResponse], "Remote Command Execution", "The response contains potential Remote Command Execution vulnerabilities.", "High")]
        else:
            return None

    def doActiveScan(self, baseRequestResponse, insertionPoint):
        return None

    def consolidateDuplicateIssues(self, existingIssue, newIssue):
        if existingIssue.getIssueName() == newIssue.getIssueName():
            return -1
        else:
            return 0
class CustomScanIssue (IScanIssue):
    def init(self, httpService, url, httpMessages, name, detail, severity):
        self._httpService = httpService
        self._url = url
        self._httpMessages = httpMessages
        self._name = name
        self._detail = detail
        self._severity = severity

    def getUrl(self):
        return self._url

    def getIssueName(self):
        return self._name

    def getIssueType(self):
        return 0

    def getSeverity(self):
        return self._severity

    def getConfidence(self):
        return "Certain"

    def getIssueBackground(self):
        return None

    def getRemediationBackground(self):
        return None
    def getIssueDetail(self):
        return self._detail

    def getRemediationDetail(self):
        return None

    def getHttpMessages(self):
        return self._httpMessages

    def getHttpService(self):
        return self._httpService


