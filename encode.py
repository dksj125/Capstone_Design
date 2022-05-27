import base64

def ToBase64(file, txt):
    with open(file, 'rb') as fileObj:
        image_data=fileObj.read(1000000)
        base64_data=base64.b64encode(image_data)
        fout= open(txt, 'w')
        fout.write(base64_data.decode())
        fout.close()


def ToFile(txt, file):
    with open(txt, 'rb' ) as fileObj:
        base64_data=fileObj.read()
        ori_video_data=base64.b64decode(base64_data)
        fout= open(file, 'wb')
        fout.write(ori_video_data)
        fout.close()


ToBase64( "D:/Capstone/Capstone_Design/Movie/Comic/[상여자] 식사.mp4",'desk_base64.txt')  # Convert the file to base64

ToFile("./desk_base64.txt",'desk_cp_by_base64.mp4')  # Convert base64 encoding to a binary file
