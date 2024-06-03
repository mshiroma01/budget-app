import React, { useState } from 'react';
import { Storage } from 'aws-amplify';

const UploadFile = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);

    try {
      const result = await Storage.put(selectedFile.name, selectedFile, {
        contentType: 'text/csv',
      });
      console.log('File uploaded successfully', result);
    } catch (error) {
      console.error('Error uploading file', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={!selectedFile || uploading}>
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
    </div>
  );
};

export default UploadFile;