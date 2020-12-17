from rest_framework import serializers

# (instance=user_friends, many=True, context={"chat_user": chat_user})
# user_friends 是 Relationship 查询得到的结果集

class FriendSerializer(serializers.Serializer):
    """
    序列化-好友列表-好友信息
    """
    # 用户id
    # friend_id = serializers.SerializerMethodField(method_name="get_id")

    user_id = serializers.IntegerField(source="user.id")
    friend_id = serializers.IntegerField(source="friend.id")

    # 用户昵称
    # friend_name = serializers.SerializerMethodField(method_name="get_name")

    # 用户头像
    # friend_avatar = serializers.SerializerMethodField(method_name="get_avatar")

    # user_avatar = serializers.ImageField(source="user.user.avatar")
    # friend_avatar = serializers.ImageField(source="friend.user.avatar")

    # 用户地区
    # friend_area = serializers.SerializerMethodField(method_name="get_area")

    # 用户状态
    # friend_status = serializers.SerializerMethodField(method_name="get_status")

    # 用户备注
    friend_label = serializers.SerializerMethodField(method_name="get_label")

    # 用户来源
    # friend_resource = serializers.CharField(source="resource")

    def get_id(self, obj):
        """
        获取好友id
        :param obj:
        :return:
        """
        if obj.user.chat_id == self.context['chat_user'].id:
            # user_id是当前用户
            return obj.friend.id
        return obj.user.id

    def get_name(self, obj):
        """
        获取好友昵称
        :param obj:
        :return:
        """
        if obj.user.id == self.context['chat_user'].id:
            # user_id是当前用户
            return obj.friend.user.nickname
        return obj.user.user.nickname

    def get_avatar(self, obj):
        """
        获取好友头像
        :param obj:
        :return:
        """
        if obj.user.id == self.context['chat_user'].id:
            # user_id是当前用户
            return obj.friend.user.avatar
        return obj.user.user.avatar

    def get_area(self, obj):
        """
        获取好友地区
        :param obj:
        :return:
        """
        if obj.user.id == self.context['chat_user'].id:
            # user_id是当前用户
            return obj.friend.area
        return obj.user.area

    def get_status(self, obj):
        """
        获取好友状态
        :param obj:
        :return:
        """
        if obj.user.id == self.context['chat_user'].id:
            # user_id是当前用户
            return obj.friend.status
        return obj.user.status

    def get_label(self, obj):
        """
        获取好友备注
        :param obj:
        :return:
        """
        if obj.user.id == self.context['chat_user'].id:
            # user_id是当前用户
            return obj.friend_label
        return obj.user_label

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass