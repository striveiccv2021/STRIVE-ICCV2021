import cv2
import os
import boto3
import glob


RESULTS_FOLDER = '../results/' # path to store the frame, crop files
SRC_FOLDER = '../sources/' # path of all videos

"""
upload to S3 bucket
"""
def upload_s3(videoName):
    PATH = SRC_FOLDER+'/' + videoName

    s3_client = boto3.client('s3', aws_access_key_id=AWS_KEY, aws_secret_access_key=SECRET_KEY);
    for r, d, f in os.walk(PATH):
        for filename in f:
            file_name = os.path.join(r, filename);
            s3_client.upload_file(file_name, BUCKET_NAME, filename);
            files.append(filename);
    print('Files uploaded successfully')
    return "Uploaded successfully"


"""
Method to call AWS S3 for tet rekognition API
"""
def call_s3Detect(fileName,videoName, targetText, count):

    client = boto3.client('rekognition', region_name=region, aws_access_key_id=AWS_KEY,
                          aws_secret_access_key=SECRET_KEY)

    response = client.detect_text(Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': fileName}})
    textDetections = response['TextDetections']
    if not os.path.isdir( RESULTS_FOLDER+'/' + videoName):
        os.mkdir(RESULTS_FOLDER+'/' +  videoName)
    text_file_name = RESULTS_FOLDER+'/' +  videoName + '/' + fileName.replace('.jpg', '.txt')
    #output_textfile = RESULTS_FOLDER+'/' + videoName +'_output.json';
    text_file = open(str(text_file_name), "w+")
    #output_file = open(str(output_textfile) , "w+")
    # text_file.write("Hello \n")
    # text_file.writelines(L)
    # text_file.close()
    # print(text_file_name)
    for text in textDetections:
        print(text)

        text_geometry = text['Geometry']

        if (targetText == '' or text['DetectedText'].lower() == targetText.lower()):
            # output_file.write('{text: '+text['DetectedText']+',confidence: '+ "{:.2f}".format(text['Confidence'])+',points:[{ x:'+str(text_geometry['Polygon'][0]['X']) +
            #                   ',y:' + str(text_geometry['Polygon'][0]['Y']) + '},{ x:' + str(
            #         text_geometry['Polygon'][1]['X']) + ',y:' + str(text_geometry['Polygon'][1]['Y']) + '},{ x:' + str(
            #         text_geometry['Polygon'][2]['X']) + ',y:' + str(text_geometry['Polygon'][2]['Y']) + '},{ x:' + str(
            #         text_geometry['Polygon'][3]['X']) + ',y:' + str(text_geometry['Polygon'][3]['Y']))+' }]}'
            text_file.write(
                str(text_geometry['Polygon'][0]['X']) + ',' + str(text_geometry['Polygon'][0]['Y']) + ',' + str(
                    text_geometry['Polygon'][1]['X']) + ',' + str(text_geometry['Polygon'][1]['Y']) + ',' + str(
                    text_geometry['Polygon'][2]['X']) + ',' + str(text_geometry['Polygon'][2]['Y']) + ',' + str(
                    text_geometry['Polygon'][3]['X']) + ',' + str(text_geometry['Polygon'][3]['Y']) + ',' + text[
                    'Type'] + ',' + text['DetectedText'] + ',' + "{:.2f}".format(text['Confidence']) + '\n')


    text_file.close()
    #output_file.close()
    # if(count > 20):
    #   break;


    return "done"


"""
Extract roi from AWS result for the target text
"""

def extract_roi_aws(aws_result_folder, requestFolderName, targetText):
    lowercaseword = targetText.lower()
    if lowercaseword == 'altman': file_prefix= 'seg_3_Altman_frame_'
    if lowercaseword == 'oscar': file_prefix = 'seg_0_Oscar_frame_'
    print(aws_result_folder)
    for file in os.listdir(aws_result_folder):
        frame_num = file.split('_')[-1].replace('.txt', '')
        filename = file_prefix + frame_num
        print(filename)

        frame_file = os.path.join(requestFolderName,'frame','IMG_frame_'+ frame_num + '.jpg')
        bg_file = os.path.join(requestFolderName, 'bg', 'IMG_bg_' + frame_num + '.jpg')
        aws_result = os.path.join(aws_result_folder, filename + '.txt')
        img = cv2.imread(frame_file)
        bg_img = cv2.imread(bg_file)
        height, width, c = img.shape
        print(width, height)

        roi_dir = os.path.join(requestFolderName,'roi')

        if not os.path.exists(roi_dir): os.mkdir(roi_dir)
        crop_dir = os.path.join(requestFolderName,'crop')
        if not os.path.exists(crop_dir): os.mkdir(crop_dir)

        frame_crop_file = os.path.join(crop_dir, 'IMG_crop_' + frame_num + '.jpg')
        bg_crop_file = os.path.join(requestFolderName, 'bg', 'IMG_crop_' + frame_num + '.jpg')

        with open(aws_result, "r") as f:

            lines = f.readlines()
            print(len(lines))
            for line in lines:

                params = line.split(',')
                if (params[8] == 'WORD'):
                    # print("**********")
                    # print(line)
                    # print("Detected word: ",params[9])
                    if params[9].lower() == lowercaseword:



                        point_x1, point_y1 = int(width * float(params[0])), int(height * float(params[1]))
                        point_x2, point_y2 = int(width * float(params[2])), int(height * float(params[3]))
                        point_x3, point_y3 = int(width * float(params[4])), int(height * float(params[5]))
                        point_x4, point_y4 = int(width * float(params[6])), int(height * float(params[7]))

                        print("points: ",point_x1,point_y1,point_x2,point_y2,point_x3,point_y3,point_x4,point_y4)
                        minX, minY = point_x1, point_y1

                        # print('old value ',minX,minY)

                        if (point_x2 < minX): minX = point_x2
                        if (point_x3 < minX): minX = point_x3
                        if (point_x4 < minX): minX = point_x4

                        if (point_y2 < minY): minY = point_y2
                        if (point_y3 < minY): minY = point_y3
                        if (point_y4 < minY): minY = point_y4

                        maxX, maxY = point_x1, point_y1



                        if (point_x2 > maxX): maxX = point_x2
                        if (point_x3 > maxX): maxX = point_x3
                        if (point_x4 > maxX): maxX = point_x4

                        if (point_y2 > maxY): maxY = point_y2
                        if (point_y3 > maxY): maxY = point_y3
                        if (point_y4 > maxY): maxY = point_y4



                        width1 = maxX - minX
                        height1 = maxY - minY
                        padding = 10

                        roi_file = open(os.path.join(roi_dir, 'frame_' + frame_num + '.txt'), 'w+')
                        roi_file.write("'" + lowercaseword + "'  [" + str(minX - padding) + "," + str(minY - padding) + "," + str(
                            maxX + padding) + "," + str(maxY + padding) +"]")
                        roi_file.close()

                        c1 = img[minY - padding:maxY + padding, minX - padding:maxX + padding]
                        c2 = bg_img[minY - padding:maxY + padding, minX - padding:maxX + padding]

                        cv2.imwrite(frame_crop_file, c1)
                        cv2.imwrite(bg_crop_file, c2)




            f.close()