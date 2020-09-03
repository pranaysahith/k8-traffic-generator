import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";

export default function FileUploader() {
  const onDrop = useCallback((acceptedFiles) => {
    alert("Thank you, the files were uploaded!");
    acceptedFiles.forEach((file) => {
      const reader = new FileReader();

      reader.onabort = () => console.log("file reading was aborted");
      reader.onerror = () => console.log("file reading has failed");
      reader.onload = () => {
        // Do whatever you want with the file contents
        const binaryStr = reader.result;
        console.log(binaryStr);
      };
      reader.readAsArrayBuffer(file);
    });
  }, []);
  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()} className="dropzone">
      <input {...getInputProps()} />
      <p>
        Welcome to the File Drop traffic generator, add as many files as you
        want!
      </p>
    </div>
  );
}
