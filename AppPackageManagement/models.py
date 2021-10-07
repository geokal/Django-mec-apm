import uuid
from django.db import models
from django_enum_choices.fields import EnumChoiceField
from enum import Enum


class Action(Enum):
    DROP = 'DROP'
    FORWARD_DECAPSULATED = 'FORWARD_DECAPSULATED'
    FORWARD_AS_IS = 'FORWARD_AS_IS'
    PASSTHROUGH = 'PASSTHROUGH'
    DUPLICATED_DECAPSULATED = 'DUPLICATED_DECAPSULATED'
    DUPLICATE_AS_IS = 'DUPLICATE_AS_IS'


class OnboardingState(Enum):
    CREATED = 'CREATED'
    UPLOADING = 'UPLOADING'
    PROCESSING = 'PROCESSING'
    ONBOARDED = 'ONBOARDED'


class UsageState(Enum):
    IN_USE = 'IN_USE'
    NOT_IN_USE = 'NOT_IN_USE'


class AppPkgOperationalState(Enum):
    DISABLED = 'Disabled'
    ENABLED = 'Enabled'


class AppPkgNotificationType(Enum):
    APP_PACKAGE_ONBOARDED = 'AppPackageOnBoarded'
    APP_PACKAGE_ENABLED = 'AppPackageEnabled'
    APP_PACKAGE_DISABLED = 'AppPackageDisabled'
    APP_PACKAGE_DELETED = 'AppPackageDeleted'


class AppPkgSubsctiptionType(Enum):
    APP_PACKAGE_ONBOARDING = 'AppPackageOnBoarding'
    APP_PACKAGE_OPERATION_CHANGE = 'AppPackageOnBoarding'
    APP_PACKAGE_DELETION = 'AppPackageDeletion'


class SubscriptionsAppPkgSubscriptionType(Enum):
    APP_PACKAGE_ONBOARDING = 'AppPackageOnBoarding'
    APP_PACKAGE_OPERATION_CHANGE = 'AppPackageOnBoarding'
    APP_PACKAGE_DELETION = 'AppPackageDeletion'


class serializerType(Enum):
    JSON = 'JSON'
    XML = 'XML'
    PROTOBUF3 = 'PROTOBUF3'


class filterType(Enum):
    FLOW = 'FLOW'
    PACKET = 'PACKET'


class IpAddressType(Enum):
    IP_V6 = 'IP_V6'
    IP_V4 = 'IP_V4'


class InterfaceType(Enum):
    TUNNEL = 'TUNNEL'
    MAC = 'MAC'
    IP = 'IP'


class TunnelType(Enum):
    GTPU = 'GTP-U'
    GRE = 'GRE'


## Actual  Django Models
class AppD(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appDescription = models.CharField(max_length=55)
    appSoftVersion = models.CharField(max_length=55)
    changeAppInstanceStateOpConfig = models.TextField(null=True, blank=True)
    mecVersion = models.CharField(max_length=55)
    swImageDescriptor = models.TextField(null=True)
    terminateAppInstanceOpConfig = models.TextField(null=True, blank=True)
    virtualComputeDescriptor = models.TextField()
    virtualStorageDescriptor = models.TextField(null=True, blank=True)


class AppPkgInfo(models.Model):
    appDId = models.OneToOneField(
        AppD,
        null=False,
        on_delete=models.CASCADE,
        related_name='appD_fk_appDid',
    )
    appProvider = models.OneToOneField(AppD,
                                       on_delete=models.CASCADE,
                                       related_name='appD_fk_appProvider')
    appName = models.OneToOneField(AppD,
                                   on_delete=models.CASCADE,
                                   related_name='appD_fk_appName')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appSoftwareVersion = models.CharField(max_length=55)

    appDVersion = models.CharField(max_length=55)

    onboardingState = EnumChoiceField(
        OnboardingState,
        default=OnboardingState.CREATED,
    )
    operationalState = EnumChoiceField(AppPkgOperationalState,
                                       default=AppPkgOperationalState.DISABLED)
    usageState = EnumChoiceField(UsageState, default=UsageState.NOT_IN_USE)


class AppPkgInfo_links(models.Model):
    _links = models.OneToOneField(
        AppPkgInfo,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='AppPkgInfo_fk_links',
    )


class AppPkgInfoModifications(models.Model):
    operationState = EnumChoiceField(AppPkgOperationalState,
                                     default=AppPkgOperationalState.DISABLED)


class AppPkgSWImageInfo(models.Model):
    softwareImages = models.ForeignKey(
        AppPkgInfo,
        null=False,
        on_delete=models.CASCADE,
        related_name='AppPkgInfo_fk_softwareImages')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(null=True, blank=True)


class AppPkgArtifactInfo(models.Model):
    additionalArtifacts = models.ForeignKey(
        AppPkgInfo,
        null=True,
        on_delete=models.CASCADE,
        related_name='AppPkgInfo_fk_additionalArtifact')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)


## AppPkgNotifications models
class AppPkgNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notificationType = EnumChoiceField(
        AppPkgNotificationType,
        default=AppPkgNotificationType.APP_PACKAGE_DISABLED)
    subscriptionId = models.CharField(max_length=55)
    appPkgId = models.CharField(max_length=55)
    appDId = models.CharField(max_length=55)
    operationalState = EnumChoiceField(AppPkgOperationalState,
                                       default=AppPkgOperationalState.DISABLED)


class AppPkgNotification_links(models.Model):
    #One2One
    _links = models.OneToOneField(
        AppPkgNotification,
        on_delete=models.CASCADE,
        related_name='AppPkgNotification_links_fk_links')


## AppPkgSubscriptions
class AppPkgSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    callbackUri = models.TextField()


class AppPkgSubscriptionInfo(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscriptionType = EnumChoiceField(AppPkgSubsctiptionType, default=None)
    callbackUri = models.TextField()


class AppPkgSubscriptionInfo_links(models.Model):
    _links = models.OneToOneField(
        AppPkgSubscriptionInfo,
        on_delete=models.CASCADE,
        related_name='AppPkgSubscriptionInfo_fk_links')


class AppPkgSubscriptionLinkList(models.Model):
    _links = models.URLField()


class SubscriptionsAppPkgSubscription(models.Model):
    href = models.URLField()
    subscriptionType = EnumChoiceField(SubscriptionsAppPkgSubscriptionType,
                                       default=None)


class AppPkgSubscriptionLinkList_links(models.Model):

    subscriptions = models.OneToOneField(
        SubscriptionsAppPkgSubscription,
        on_delete=models.CASCADE,
        related_name='SubscriptionsAppPkgSubscription_fk_subscriptions')


class AppExternalCpd(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appExtCpd = models.ForeignKey(AppD,
                                  on_delete=models.CASCADE,
                                  related_name='appD_fk_appExtCpd',
                                  null=True)
    inherited_attributes = models.TextField()
    virtualNetworkInterfaceRequirements = models.TextField(blank=True)


class CategoryRef(models.Model):
    pass


class CreateAppPkg(models.Model):
    appPkgName = models.CharField(max_length=55)
    appPkgPath = models.URLField()
    appPkgVersion = models.CharField(max_length=55)
    appProvider = models.CharField(max_length=55)
    userDefinedData = models.CharField(max_length=55)


class Checksum(models.Model):
    appPkgInfo_fk_checksum = models.OneToOneField(
        AppPkgInfo,
        blank=True,
        on_delete=models.CASCADE,
        null=True,
        related_name='appPkgInfo_fk_checksum')
    createAppPkg_fk_checksum = models.OneToOneField(
        CreateAppPkg,
        on_delete=models.CASCADE,
        null=True,
        related_name='createAppPkg_fk_checksum')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    algorithm = models.TextField()
    _hash = models.TextField()


class DNSRuleDescriptor(models.Model):
    appDNSRule = models.ForeignKey(AppD,
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   related_name='appD_fk_app_dns_rule')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dnsRuleId = models.CharField(max_length=55)
    domainName = models.CharField(max_length=55)
    ipAddress = models.CharField(max_length=55)
    ipAddressType = EnumChoiceField(IpAddressType, default=None)
    ttl = models.IntegerField()


class FeatureDependency(models.Model):
    appFeatureOptional = models.ForeignKey(
        AppD,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='appd_fk_app_feature_optional')
    appFeatureRequired = models.ForeignKey(
        AppD,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='appd_fk_app_feature_required')
    featureName = models.CharField(max_length=55)
    version = models.CharField(max_length=55)


class LatencyDescriptor(models.Model):
    appLatency = models.OneToOneField(AppD,
                                      on_delete=models.CASCADE,
                                      null=False)
    maxLatency = models.IntegerField()


class ProblemDetails(models.Model):
    instance = models.CharField(max_length=55)
    title = models.CharField(max_length=55)
    detail = models.TextField()
    status = models.CharField(max_length=55)
    _type = models.CharField(max_length=55)


class ServiceDescriptor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appServiceProduced = models.ManyToManyField(
        AppD, blank=True, related_name='appD_fk_app_service_produced')
    serName = models.CharField(max_length=55)
    serCategory = models.ManyToManyField(CategoryRef)
    version = models.CharField(max_length=55)


class TransportsSupported(models.Model):
    description = models.TextField(blank=True, null=True)
    transportsSupported = models.OneToOneField(
        ServiceDescriptor,
        on_delete=models.CASCADE,
        related_name='serviceDescriptor_fk_transportsSupported')


class TransportDescriptor(models.Model):
    transport = models.OneToOneField(
        TransportsSupported,
        on_delete=models.CASCADE,
        related_name='transportsSupported_fk_transport')
    security = models.OneToOneField('SecurityInfo', on_delete=models.CASCADE)
    _type = models.CharField(max_length=55)
    protocol = models.CharField(max_length=55)
    version = models.CharField(max_length=55)


class TransportDependency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transportDependencies = models.ManyToManyField(
        AppD, blank=True, related_name='appD_fk_transportDependencies')
    transport = models.OneToOneField(
        TransportDescriptor,
        on_delete=models.CASCADE,
        null=False,
        related_name='transportDescriptor_fk_transport')
    labels = models.CharField(max_length=55)
    serializers = models.CharField(default='JSON', max_length=6)


class ServiceDependency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appServiceOptional = models.ManyToManyField(
        AppD, blank=True, related_name='appD_fk_app_service_optional')
    appServiceRequired = models.ManyToManyField(
        AppD, blank=True, related_name='appD_fk_app_service_required')
    serTransportDependencies = models.OneToOneField(TransportDependency,
                                                    on_delete=models.CASCADE)
    requestedPermissions = models.TextField(blank=True)
    serCategory = models.CharField(blank=True, max_length=55)
    serName = models.CharField(max_length=55)
    version = models.CharField(max_length=55)


class TrafficRuleDescriptor(models.Model):
    appTrafficRule = models.ForeignKey(AppD,
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       related_name='appD_fk_appTrafficRule')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trafficRuleId = models.TextField()
    action = EnumChoiceField(Action, default=None)
    filterType = EnumChoiceField(filterType, default=None)
    priority = models.IntegerField()


class SecurityInfo(models.Model):
    trafficRuleDescriptor_fk_security = models.ForeignKey(
        TrafficRuleDescriptor,
        on_delete=models.CASCADE,
        related_name='trafficRuleDescriptor_fk_security')
    transport_descriptor_fk_security = models.ForeignKey(
        TransportDescriptor,
        on_delete=models.CASCADE,
        related_name='transport_descriptor_fk_security')
    description = models.TextField(max_length=255)
    oAuth2Info = models.CharField(max_length=255, default=None)
    tokenEndpoint = models.URLField(default=None)
    grantTypes = models.CharField(default='OAUTH2_CLIENT_CREDENTIALS',
                                  max_length=255)


class Serializers(models.Model):
    serializers = models.ForeignKey(
        TransportsSupported,
        on_delete=models.CASCADE,
        related_name='transportsSupported_fk_serializers')
    serializerTypes = EnumChoiceField(serializerType, default=None)


class InterfaceDescriptor(models.Model):
    dstInterface = models.ForeignKey(
        TrafficRuleDescriptor,
        on_delete=models.CASCADE,
        related_name='trafficRuleDescriptor_fk_dstInterface')
    interfaceType = EnumChoiceField(InterfaceType, default=None)
    srcMACAddress = models.CharField(max_length=55)
    dstMACAddress = models.CharField(max_length=55)
    dstIPAddress = models.CharField(max_length=55)


class TunnelInfo(models.Model):
    tunnelInfo = models.OneToOneField(InterfaceDescriptor,
                                      on_delete=models.CASCADE)
    tunnelType = EnumChoiceField(TunnelType, default=None)
    tunnelDstAddress = models.CharField(max_length=55)
    tunnelSrcAddress = models.CharField(max_length=55)
    tunnelSpecificData = models.TextField(blank=True)


class TrafficFilter(models.Model):
    trafficFilter = models.ForeignKey(
        TrafficRuleDescriptor,
        on_delete=models.CASCADE,
        null=False,
        related_name='trafficFilter_fk_trafficFilter')
    srcAddress = models.CharField(blank=True, max_length=55)
    dstAddress = models.CharField(blank=True, max_length=55)
    srcPort = models.CharField(blank=True, max_length=55)
    dstPort = models.CharField(blank=True, max_length=55)
    protocol = models.CharField(blank=True, max_length=55)
    srcTunnelAddress = models.CharField(blank=True, max_length=55)
    tgtTunnelAddress = models.CharField(blank=True, max_length=55)
    srcTunnelPort = models.CharField(blank=True, max_length=55)
    dstTunnelPort = models.CharField(blank=True, max_length=55)
    qCI = models.IntegerField(blank=True)
    dSCP = models.IntegerField(blank=True)
    tC = models.IntegerField(blank=True)
    tag = models.CharField(blank=True, max_length=55)


class TimeStamp(models.Model):
    #TODO maybe add parameters for time managment (seconds-->time.time()
    #TODO  and nanoSec --> time.time_ns())
    #TODO ManyToMany ?
    timeStamp = models.ForeignKey(AppPkgNotification,
                                  on_delete=models.CASCADE,
                                  related_name='+')
    nanoSeconds = models.IntegerField()
    seconds = models.IntegerField()


class KeyValuePairs(models.Model):
    userDefinedData = models.ForeignKey(
        AppPkgInfo,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='app_pkg_info_fk_userdefinedata')
    additionalProperties = models.TextField(null=True, blank=True)


class LinkType(models.Model):
    _self = models.ForeignKey(AppPkgInfo_links,
                              on_delete=models.CASCADE,
                              related_name='app_pkg_info_links_fk_self')

    appD = models.ForeignKey(AppPkgInfo_links,
                             on_delete=models.CASCADE,
                             related_name='app_pkg_info_links_fk_appD')

    appPkgContent = models.ForeignKey(
        AppPkgInfo_links,
        on_delete=models.CASCADE,
        related_name='app_pkg_info_links_fk_appPkgContent')

    appPkgNotification_links_subscription = models.ForeignKey(
        AppPkgNotification_links,
        on_delete=models.CASCADE,
        related_name='app_pkg_notification_links_fk_subscription')

    appPkgSubscriptionInfo_links_self = models.ForeignKey(
        AppPkgSubscriptionInfo_links,
        on_delete=models.CASCADE,
        related_name='app_pkg_subscription_info_links_fk_self')

    appPkgSubscriptionLinkList_links_self = models.ForeignKey(
        AppPkgSubscriptionLinkList_links,
        on_delete=models.CASCADE,
        related_name='app_pkg_subscription_linklist_links_fk_self')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    href = models.URLField()
