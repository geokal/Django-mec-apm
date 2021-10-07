import json
import os
#from typing_extensions import Required
from django.db.models import fields

from rest_framework import serializers

from AppPackageManagement.models import *
from utils.file_manipulation import create_dir
from utils.format_tools import transform_representation

apm_package_base_path = os.getcwd() + "/ApmPackage/"
create_dir(apm_package_base_path)


class AppExternalCpdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppExternalCpd
        fields = (
            'inherited_attributes',
            'virtualNetworkInterfaceRequirements',
        )


class CategoryRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRef
        fields = "__all__"


class ChecksumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checksum
        fields = (
            'algorithm',
            '_hash',
        )


class DNSRuleDescriptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNSRuleDescriptor
        fields = (
            'dnsRuleId',
            'domainName',
            'ipAddress',
            'ipAddressType',
            'ttl',
        )


class FeatureDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureDependency
        fields = (
            'featureName',
            'version',
        )


class KeyValuePairsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyValuePairs
        fields = "__all__"


class LatencyDescriptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatencyDescriptor
        fields = ('maxLatency', )


class ProblemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemDetails
        fields = (
            'detail'
            'instance',
            'status',
            'title',
            'type',
        )


class ServiceDependencySerializer(serializers.ModelSerializer):
    serCategory = CategoryRefSerializer()

    class Meta:
        model = ServiceDependency
        fields = '__all__'


class TimeStampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeStamp
        fields = ('nanoSeconds', 'seconds')


class TrafficFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFilter
        fields = (
            'dSCP',
            'dstAddress',
            'dstPort',
            'dstTunnelPort',
            'protocol',
            'qCI',
            'srcAddress',
            'srcPort',
            'srcTunnelAddress',
            'srcTunnelPort',
            'tC',
            'tag',
            'tgtTunnelAddress',
        )


class TransportDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportDependency
        fields = (
            'labels',
            'serializers',
            'transport',
        )


class SecurityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityInfo
        fields = (
            'description',
            'oAuth2Info',
            'tokenEndpoint',
            'grantTypes',
        )


class TransportDescriptorSerializer(serializers.ModelSerializer):
    security = SecurityInfoSerializer()

    class Meta:
        model = TransportDescriptor
        fields = (
            'protocol',
            'security',
            '_type',
            'version',
        )


class TransportsSupportedSerializer(serializers.ModelSerializer):
    transport = TransportDescriptorSerializer()

    class Meta:
        model = TransportsSupported
        fields = ('transport', )


class ServiceDescriptorSerializer(serializers.ModelSerializer):
    serCategory = CategoryRefSerializer()
    transportsSupported = TransportsSupportedSerializer()

    class Meta:
        model = ServiceDescriptor
        fields = (
            'serName',
            'serCategory',
            'version',
            'transportsSupported',
        )


class TunnelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TunnelInfo
        fields = (
            'tunnelType',
            'tunnelDstAddress',
            'tunnelSrcAddress',
            'tunnelSpecificData',
        )


class InterfaceDescriptorSerializer(serializers.ModelSerializer):
    tunnelInfo = TunnelInfoSerializer()

    class Meta:
        model = InterfaceDescriptor
        fields = (
            'dstIPAddress',
            'dstMACAddress',
            'interfaceType',
            'srcMACAddress',
            'tunnelInfo',
        )


class TrafficRuleDescriptorSerializer(serializers.ModelSerializer):
    dstInterface = InterfaceDescriptorSerializer()
    filterType = TrafficFilterSerializer()
    trafficFilter = TrafficFilterSerializer()

    class Meta:
        model = TrafficRuleDescriptor
        fields = (
            'action',
            'trafficRuleId',
            'dstInterface',
            'filterType',
            'priority',
            'trafficFilter',
        )


class LinkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkType
        fields = "__all__"


class AppPkgInfoModificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPkgInfoModifications
        fields = "__all__"


class AppPkgNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPkgNotification
        fields = (
            'notificationType',
            'subscriptionId',
            'timeStamp',
            'appPkgId',
            'appDId',
            'operationalState',
            '_links',
        )


class AppPkgNotificationLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPkgNotification_links
        fields = ('subscription', )


class AppPkgSubscriptionInfoLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPkgSubscriptionInfo_links
        fields = ('self', )


class AppPkgSubscriptionLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPkgSubscriptionInfo_links
        fields = ('_links', )


class AppPkgSubscriptionLinkListLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPkgSubscriptionLinkList
        fields = (
            'self',
            'subscriptions',
        )


class SubscriptionsAppPkgSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionsAppPkgSubscription
        fields = (
            'href',
            'subsctiptionType',
        )


class AppPkgSubscriptionInfoSerializer(serializers.ModelSerializer):
    _links = AppPkgSubscriptionInfoLinksSerializer()

    class Meta:
        model = AppPkgSubscriptionInfo
        fields = (
            'callbackUri',
            'subsctiptionType',
            'appPkgFilter',
            '_links',
        )


class CreateAppPkgSerializer(serializers.ModelSerializer):
    checksum = ChecksumSerializer(source='createAppPkg_fk_checksum')
    userDefinedData = KeyValuePairsSerializer()

    class Meta:
        model = CreateAppPkg
        fields = (
            'appPkgName',
            'appPkgPath',
            'appPkgVersion',
            'appProvider',
            'checksum',
            'userDefinedData',
        )


class AppPkgInfoLinksSerializer(serializers.ModelSerializer):

    _self = LinkTypeSerializer(source='app_pkg_info_links_fk_self')

    appD = LinkTypeSerializer(source='app_pkg_info_links_fk_appD')
    appPkgContent = LinkTypeSerializer(
        source='app_pkg_info_links_fk_appPkgContent')

    class Meta:
        model = AppPkgInfo_links
        fields = (
            '_self',
            'appD',
            'appPkgContent',
        )


class AppPkgSWImageInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPkgSWImageInfo
        fields = ('description', )

    def to_representation(self, instance):
        return transform_representation(super().to_representation(instance))


class AppPkgArtifactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPkgArtifactInfo
        fields = ('description', )


class AppPkgInfoSerializer(serializers.ModelSerializer):
    checksum = ChecksumSerializer(required=True,
                                  source='appPkgInfo_fk_checksum')
    additionalArtifacts = AppPkgArtifactInfoSerializer(
        many=True, required=False, source='AppPkgInfo_fk_additionalArtifact')
    softwareImages = AppPkgSWImageInfoSerializer(
        many=True, required=False, source='AppPkgInfo_fk_softwareImages')
    _links = AppPkgInfoLinksSerializer(required=False,
                                       source='AppPkgInfo_fk_links')
    userDefinedData = KeyValuePairsSerializer(many=True, required=False)

    class Meta:
        model = AppPkgInfo
        fields = '__all__'

    def to_representation(self, instance):
        return transform_representation(super().to_representation(instance))

    def create(self, validated_data):
        link_value = validated_data.pop('AppPkgInfo_fk_links')
        app_package_info = AppPkgInfo_links.objects.create(**validated_data)
        path_content = ['appD', 'appPkgContent']

        for dir_name in path_content:
            create_dir('{}{}/{}'.format(apm_package_base_path,
                                        app_package_info.id, dir_name))

        #TODO need fix in links self
        AppPkgInfo_links.objects.create(
            _links=app_package_info,
            **{
                'appPkgInfo_links_self':
                '{}{}'.format(link_value['appPkgInfo_links_self'],
                              app_package_info.id),
                'appD':
                '{}{}/{}'.format(link_value[path_content[0]],
                                 app_package_info.id, path_content[0]),
                'appPkgContent':
                '{}{}/{}'.format(link_value['appPkgContent'],
                                 app_package_info.id, path_content[1])
            })
        return app_package_info

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class AppDSerializer(serializers.ModelSerializer):
    appDId = AppPkgInfoSerializer()
    appProvider = AppPkgInfoSerializer()
    appName = AppPkgInfoSerializer()
    appExtCpd = AppExternalCpdSerializer()
    appDNSRule = DNSRuleDescriptorSerializer()
    appLatency = LatencyDescriptorSerializer()
    appTrafficRule = TrafficRuleDescriptorSerializer()
    appServiceProduced = ServiceDescriptorSerializer()
    transportDependencies = TransportDependencySerializer()
    appServiceOptional = ServiceDependencySerializer()
    appServiceRequired = ServiceDependencySerializer()

    class Meta:
        model = AppD
        fields = '__all__'

    def to_representation(self, instance):
        return transform_representation(super().to_representation(instance))
