__author__ = "Bradley Rose"
__version__ = "0.1"
"""
Please see usage details in the readme provided!
This API was built using the provided API documentation.
"""

import requests

class Prime:
    def __init__(self,*, username, password, primeUrl):
        self.apiPassword = password
        self.apiUser = username
        self.urlBase = primeUrl + "/webacs/api/"

    """
    --------------------------
    | HTTP Standard Requests |
    --------------------------
    These are the basic GET, POST, PUT, and DELETE used for CRUD.
    These are used by other methods defined beneath these to perform operations.
    """

    def get(self, url):
        """
        Description
        -----------
        HTTP GET operations on a provided URL.

        Parameters
        ----------
        url: string
            A provided URL string for a particular resource.

        Returns
        -------
        If HTTP status code == 200:
            data: dictionary
                Dictionary of key:value pairs of all attributes of resource where GET operation was performed.
        else:
            message: string
                An Prime error message.
        """
        request = requests.get(
            url = url,
            headers={
                'Accept':'application/json'
            },
            auth=(
                self.apiUser,
                self.apiPassword
            ),
            verify=False
        )

        if request.status_code == 200:
            return request.json()
        else:
            return request.status_code

    def getAllPrimeDevices(self):
        """
        Description
        -----------
        Obtains all objects from Cisco Prime.

        Parameters
        ----------
        None

        Returns
        -------
        allDevices: dictionary
            Dictionary element of each device object and its inventory attributes
        """
        url = self.urlBase + 'v4/data/Devices/'
        results = self.get(url)
        allDevices = []
        for device in results['queryResponse']['entityId']:
            deviceResult = self.get(device['@url'])['entity'][0]['devicesDTO']
            allDevices.append(deviceResult)
        return allDevices
        
    def getJobStatus(self, *, jobId):
        """
        Description
        -----------
        Obtains backup job properties from Cisco Prime.

        Parameters
        ----------
        None

        Returns
        -------
        response: list
            List object of all jobs matching the request.
        """
        url = self.urlBase + "v4/op/jobService/runhistory.json"
        if jobId:
            url += "?jobId=" + str(jobId)
        return self.get(url)['mgmtResponse']