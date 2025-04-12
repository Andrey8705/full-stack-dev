import { useDropzone } from 'react-dropzone';
import { useState, useEffect } from 'react';
import { API_BASE_URL } from '@/app/service/AuthFetch';
import { toast } from 'react-toastify';

interface FileUploaderProps {
  label: string;
  accept: string | string[];
  maxFiles?: number;
  multiple?: boolean;
  defaultPreviewUrls?: string[];
  onUploadSuccess?: (response: any) => void;
}

const formatAccept = (accept: string | string[]) => {
  if (typeof accept === 'string') {
    return { [accept]: [] };
  } else {
    return accept.reduce((acc, type) => ({ ...acc, [type]: [] }), {});
  }
};

export const FileUploader = ({
  label,
  accept,
  maxFiles = 1,
  multiple = false,
  defaultPreviewUrls = [],
  onUploadSuccess,
}: FileUploaderProps) => {
  const [previewUrls, setPreviewUrls] = useState<string[]>(defaultPreviewUrls);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = (acceptedFiles: File[]) => {
    const limitedFiles = acceptedFiles.slice(0, maxFiles);
    setSelectedFiles(limitedFiles);
    setPreviewUrls(limitedFiles.map(file => URL.createObjectURL(file)));
  };

  const { getRootProps, getInputProps } = useDropzone({
    accept: formatAccept(accept),
    onDrop,
    multiple,
    maxFiles,
  });

  const handleUpload = async () => {
    if (!selectedFiles.length) return;

    const formData = new FormData();
    formData.append("file", selectedFiles[0]);

    setIsUploading(true);
    try {
      const response = await fetch(`${API_BASE_URL}upload-avatar`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token") || ""}`,
        },
        body: formData,
      });

      if (!response.ok) throw new Error("Ошибка загрузки файла");

      const data = await response.json();

      // Успешно загружено — вызываем callback
      if (onUploadSuccess) onUploadSuccess(data);
      toast.success("Аватар успешно загружен!");
    } catch (error) {
      console.error("Ошибка при загрузке:", error);
      alert("Ошибка загрузки файла");
    } finally {
      setIsUploading(false);
    }
  };

  useEffect(() => {
    return () => {
      previewUrls.forEach(url => URL.revokeObjectURL(url));
    };
  }, [previewUrls]);

  return (
    <div className="p-4 border-2 border-dashed rounded-xl">
      <label className="block mb-2 text-sm font-medium">{label}</label>
      <div
        {...getRootProps()}
        className="cursor-pointer p-4 bg-gray-50 hover:bg-gray-100 rounded-xl"
      >
        <input {...getInputProps()} />
        <p className="text-center text-gray-500">Перетащи файл сюда или кликни, чтобы выбрать</p>
      </div>

      <div className="mt-4 flex gap-2 flex-wrap">
        {previewUrls.map((url, i) => (
          <div key={i} className="w-24 h-24 overflow-hidden rounded-lg border">
            <img src={url} className="w-full h-full object-cover" alt="preview" />
          </div>
        ))}
      </div>

      {selectedFiles.length > 0 && (
        <button
          onClick={handleUpload}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition disabled:opacity-50"
          disabled={isUploading}
        >
          {isUploading ? "Загрузка..." : "Загрузить"}
        </button>
      )}
    </div>
  );
};

export default FileUploader;
