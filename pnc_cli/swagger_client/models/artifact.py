# coding: utf-8

"""
Copyright 2015 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from datetime import datetime
from pprint import pformat
from six import iteritems


class Artifact(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Artifact - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'int',
            'identifier': 'str',
            'repo_type': 'str',
            'checksum': 'str',
            'filename': 'str',
            'deploy_url': 'str',
            'status': 'str',
            'build_record': 'BuildRecord',
            'field_handler': 'FieldHandler'
        }

        self.attribute_map = {
            'id': 'id',
            'identifier': 'identifier',
            'repo_type': 'repoType',
            'checksum': 'checksum',
            'filename': 'filename',
            'deploy_url': 'deployUrl',
            'status': 'status',
            'build_record': 'buildRecord',
            'field_handler': 'fieldHandler'
        }

        self._id = None
        self._identifier = None
        self._repo_type = None
        self._checksum = None
        self._filename = None
        self._deploy_url = None
        self._status = None
        self._build_record = None
        self._field_handler = None

    @property
    def id(self):
        """
        Gets the id of this Artifact.


        :return: The id of this Artifact.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Artifact.


        :param id: The id of this Artifact.
        :type: int
        """
        self._id = id

    @property
    def identifier(self):
        """
        Gets the identifier of this Artifact.


        :return: The identifier of this Artifact.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this Artifact.


        :param identifier: The identifier of this Artifact.
        :type: str
        """
        self._identifier = identifier

    @property
    def repo_type(self):
        """
        Gets the repo_type of this Artifact.


        :return: The repo_type of this Artifact.
        :rtype: str
        """
        return self._repo_type

    @repo_type.setter
    def repo_type(self, repo_type):
        """
        Sets the repo_type of this Artifact.


        :param repo_type: The repo_type of this Artifact.
        :type: str
        """
        allowed_values = ["MAVEN", "DOCKER_REGISTRY", "NPM", "COCOA_POD"]
        if repo_type not in allowed_values:
            raise ValueError(
                "Invalid value for `repo_type`, must be one of {0}"
                .format(allowed_values)
            )
        self._repo_type = repo_type

    @property
    def checksum(self):
        """
        Gets the checksum of this Artifact.


        :return: The checksum of this Artifact.
        :rtype: str
        """
        return self._checksum

    @checksum.setter
    def checksum(self, checksum):
        """
        Sets the checksum of this Artifact.


        :param checksum: The checksum of this Artifact.
        :type: str
        """
        self._checksum = checksum

    @property
    def filename(self):
        """
        Gets the filename of this Artifact.


        :return: The filename of this Artifact.
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """
        Sets the filename of this Artifact.


        :param filename: The filename of this Artifact.
        :type: str
        """
        self._filename = filename

    @property
    def deploy_url(self):
        """
        Gets the deploy_url of this Artifact.


        :return: The deploy_url of this Artifact.
        :rtype: str
        """
        return self._deploy_url

    @deploy_url.setter
    def deploy_url(self, deploy_url):
        """
        Sets the deploy_url of this Artifact.


        :param deploy_url: The deploy_url of this Artifact.
        :type: str
        """
        self._deploy_url = deploy_url

    @property
    def status(self):
        """
        Gets the status of this Artifact.


        :return: The status of this Artifact.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this Artifact.


        :param status: The status of this Artifact.
        :type: str
        """
        allowed_values = ["BINARY_IMPORTED", "BINARY_BUILT"]
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status`, must be one of {0}"
                .format(allowed_values)
            )
        self._status = status

    @property
    def build_record(self):
        """
        Gets the build_record of this Artifact.


        :return: The build_record of this Artifact.
        :rtype: BuildRecord
        """
        return self._build_record

    @build_record.setter
    def build_record(self, build_record):
        """
        Sets the build_record of this Artifact.


        :param build_record: The build_record of this Artifact.
        :type: BuildRecord
        """
        self._build_record = build_record

    @property
    def field_handler(self):
        """
        Gets the field_handler of this Artifact.


        :return: The field_handler of this Artifact.
        :rtype: FieldHandler
        """
        return self._field_handler

    @field_handler.setter
    def field_handler(self, field_handler):
        """
        Sets the field_handler of this Artifact.


        :param field_handler: The field_handler of this Artifact.
        :type: FieldHandler
        """
        self._field_handler = field_handler

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
	    elif isinstance(value, datetime):
		result[attr] = str(value.date())
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()
