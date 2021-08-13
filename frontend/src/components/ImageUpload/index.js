import React, { useState } from "react";
import { Upload, message, Typography } from 'antd';
import { InboxOutlined } from '@ant-design/icons';

const { Dragger } = Upload;
const { Paragraph } = Typography;

function ImageUpload () {
    const [fileObj, setFileObj] = useState(null)
    const [showResult, setShowResult] = useState(false)
    const [className, setClassName] = useState('')
    const props = {
      name: 'file',
      multiple: false,
      action: 'http://localhost:8000/predict-img',
      type: 'image/*',
      onChange(info) {
        const { status, response, originFileObj } = info.file;
        setFileObj(URL.createObjectURL(originFileObj))
        if (status === 'uploading') {
          console.log('UPLOADING')
        }
        if (status !== 'uploading') {
          console.log(info.file, info.fileList);
        }
        if (status === 'done') {
            predictionDone(response);
            // message.success(`${info.file.name} file uploaded successfully.`);
        } else if (status === 'error') {
            message.error(`${info.file.name} file upload failed.`);
        }
      },
      onDrop(e) {
        console.log('Dropped files', e.dataTransfer.files);
      },
    };

    function predictionDone (response) {
        setShowResult(true)
        setClassName(response.likely_class)
    }

    return (
        <>
            <Dragger {...props}>
                <p className="ant-upload-drag-icon">
                  <InboxOutlined />
                </p>
                <p className="ant-upload-text">Click or drag file to this area to upload</p>
                <p className="ant-upload-hint">
                  Support for a single or bulk upload. Strictly prohibit from uploading company data or other
                  band files
                </p>
            </Dragger>
            <hr />
            {
                showResult && (
                    <div>
                        <div style={{width: "60vw", maxWidth: "300px"}}>
                            <img style={{width: "100%"}} src={fileObj} alt={'result'}/>
                        </div>
                        <Typography>
                            <Paragraph>
                              <pre>This is {className}</pre>
                            </Paragraph>
                        </Typography>

                    </div>
                )
            }
        </>
    )
}

export default ImageUpload