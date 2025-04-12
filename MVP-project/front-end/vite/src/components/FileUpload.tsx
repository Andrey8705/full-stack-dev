import { useDropzone } from 'react-dropzone';
import { useState, useEffect } from 'react';

interface FileUploaderProps {
  label: string;
  accept: string | string[];
  maxFiles?: number;
  onFilesSelected: (files: File[]) => void;
  multiple?: boolean;
  defaultPreviewUrls?: string[];
}

export const FileUploader = ({
  label,
  accept,
  maxFiles = 1,
  onFilesSelected,
  multiple = false,
  defaultPreviewUrls = [],
}: FileUploaderProps) => {
  const [previewUrls, setPreviewUrls] = useState<string[]>(defaultPreviewUrls);

  const onDrop = (acceptedFiles: File[]) => {
    const limitedFiles = acceptedFiles.slice(0, maxFiles);
    setPreviewUrls(limitedFiles.map(file => URL.createObjectURL(file)));
    onFilesSelected(limitedFiles);
  };

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      'image/*': [],
      'video/*': [],
    },
    onDrop,
    multiple,
    maxFiles,
  });

  useEffect(() => {
    return () => {
      previewUrls.forEach(url => URL.revokeObjectURL(url));
    };
  }, [previewUrls]);

  return (
    <div className="p-4 border-2 border-dashed rounded-xl">
      <label className="block mb-2 text-sm font-medium">{label}</label>
      <div {...getRootProps()} className="cursor-pointer p-4 bg-gray-50 hover:bg-gray-100 rounded-xl">
        <input {...getInputProps()} />
        <p className="text-center text-gray-500">Перетащи файл сюда или кликни, чтобы выбрать</p>
      </div>
      <div className="mt-4 flex gap-2 flex-wrap">
        {previewUrls.map((url, i) => (
          <div key={i} className="w-24 h-24 overflow-hidden rounded-lg border">
            {url.includes('video') ? (
              <video src={url} controls className="w-full h-full object-cover" />
            ) : (
              <img src={url} className="w-full h-full object-cover" alt="preview" />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default FileUploader;