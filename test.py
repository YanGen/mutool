from mutool.sender import sendEmail

# import mutool.constants as CONSTANS
# CONSTANS.mail_pass = "VPCHYMYMYZEJCIZU"
# sendEmail("test","test")


# import tensorflow as tf
# # Creates a graph.
# a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
# b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
# c = tf.matmul(a, b)
# # Creates a session with log_device_placement set to True.
# sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
# # Runs the op.
# print(sess.run(c))

from mutool.annotation import tryDo
@tryDo()
def err():
    print(1/0)
err()
exit()

from mutool.reader import searchFile
from mutool.writer import writerToText
fs = searchFile('广州科学城',include='.mtl',deepSearch=True)
for item in fs:
    name = item.split("/")[-1]
    inds = name.strip('level_.mtl').split('_')
    text = inds[1]+"_"+inds[2]
    print(text)
    writerToText("备/"+item.split("/")[-2]+"---"+name,item + open(item).read(),append=False)
    content = open(item).read().replace('map_Kd level_4_0_0','map_Kd level_4_'+text)
    writerToText(item,content,append=False)