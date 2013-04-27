import QtQuick 1.0

Rectangle {
    id: container
    width: 283
    height: 504

    color: "#ffffff"

    function positionViewAtBeginning() { 
        tweetListView.positionViewAtBeginning();
    }

    function imageLoaded(tweetid) {
        var item = getDelegateInstanceAt(tweetid)
        item.imageLoaded()
    }

    function getDelegateInstanceAt(tweetid) {
        for (var i = 0; i < tweetListView.contentItem.children.length; i++) {
            var item = tweetListView.contentItem.children[i];
            if (item.tweetid == tweetid) {
                return item;
            }
        }
        return undefined;
    }

    ListView {
        id: tweetListView
        anchors.fill: parent;
        clip: true
        cacheBuffer: 500
        model: mymodel
        delegate: TweetDelegate {

            function retweet_string() {
                if (tweetType == 1) {
                    return "//@" + tweetScreenName + ":" + tweetText;
                }
                else {
                    return "";
                }
            }

            function favorite() {
                if (isFavorite) {
                    if (mainWindow.un_favorite(tweetid)) {
                        isFavorite = false;
                    }
                }
                else {
                    if (mainWindow.favorite(tweetid)) {
                        isFavorite = true;
                    }
                }
            }

            tweetType: type
            tweetScreenName: author.name
            tweetOriginalId: type != 0 && original.id

            // 不是单条微博，有作者信息（原微博不被删），返回作者姓名；否则返回空字符串
            tweetOriginalName: (type != 0 && original.author && original.author.name) || ""
            tweetOriginalText: type != 0 && original.text
            tweetText: text
            tweetAvatar: author.avatar
            tweetid:  id
            isOwnTweet: true
            isNewTweet: true
            isFavorite: false
            tweetSinceTime: time

            onFavoriteButtonClicked: favorite()
            onRetweetButtonClicked: mainWindow.repost(tweetid, retweet_string())
            onCommentButtonClicked: mainWindow.comment(tweetid)
            onReplyButtonClicked: mainWindow.reply(original.id, tweetid)

            // not implemented
            onMoreButtonClicked: console.log("Clicked a user: " + tweetScreenName)
            onHashtagLinkClicked: console.log("Clicked a tag: " + hashtag)
            onMentionLinkClicked: console.log("Clicked a mention: " + screenname)
        }

        onMovementEnded: {
            // load more tweets
            if (atYEnd) {
                mainWindow.load_more()
            }
        }
    }

    Rectangle {
        id: scrollbar
        anchors.right: tweetListView.right
        y: tweetListView.visibleArea.yPosition * tweetListView.height
        width: 8
        height: tweetListView.visibleArea.heightRatio * tweetListView.height
        color: "black"
    }
}
