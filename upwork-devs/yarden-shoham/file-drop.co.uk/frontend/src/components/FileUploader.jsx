import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";

export default function FileUploader() {
  const onDrop = useCallback((acceptedFiles) => {
    const data = new FormData();

    for (const file of acceptedFiles) {
      data.append("files[]", file, file.name);
    }

    return fetch("/backend/files", {
      method: "POST",
      body: data,
    });
  }, []);
  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()} className="dropzone">
      <input {...getInputProps()} />
      <p>Add as many files as you want!</p>
    </div>
  );
}
