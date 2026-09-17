import React, { useState } from 'react';
import { Upload, Image as ImageIcon, CheckCircle, RefreshCw, Sparkles, Camera } from 'lucide-react';
import { api } from '../api/client';

export default function ImageDiagnosisCard({ crop, district, t, onDiagnosisComplete }) {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedSample, setSelectedSample] = useState(null);

  const sampleImages = [
    { label: t.sampleTomatoEarly, filename: 'test_leaf_tomato_early_blight.jpg', crop: 'Tomato' },
    { label: t.sampleTomatoLate, filename: 'test_leaf_tomato_late_blight.jpg', crop: 'Tomato' },
    { label: t.sampleCornRust, filename: 'test_leaf_corn_rust.jpg', crop: 'Corn/Maize' },
    { label: t.sampleHealthy, filename: 'test_leaf_healthy.jpg', crop: 'Tomato' },
  ];

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setPreviewUrl(URL.createObjectURL(selectedFile));
      setSelectedSample(null);
    }
  };

  const handleSampleClick = async (sample) => {
    setSelectedSample(sample.filename);
    setLoading(true);
    try {
      // Fetch actual sample leaf image asset from FastAPI static files
      const imgUrl = `http://127.0.0.1:8000/sample-leaves/${sample.filename}`;
      const res = await fetch(imgUrl);
      if (!res.ok) throw new Error(`Failed to fetch sample image: ${res.statusText}`);
      
      const blob = await res.blob();
      const sampleFile = new File([blob], sample.filename, { type: 'image/jpeg' });
      setFile(sampleFile);
      setPreviewUrl(URL.createObjectURL(blob));
      await runDiagnosis(sampleFile, sample.crop);
    } catch (err) {
      console.error("Error loading sample image:", err);
      alert("Could not load sample image from backend server. Please ensure backend is running.");
      setLoading(false);
    }
  };

  const runDiagnosis = async (targetFile, targetCrop = crop) => {
    const fileToUse = targetFile || file;
    if (!fileToUse) return;

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', fileToUse);
      formData.append('crop_type', targetCrop);
      formData.append('district', district);
      formData.append('state', 'Maharashtra');
      formData.append('growth_stage', 'Flowering');
      formData.append('temperature', '21.5');
      formData.append('humidity', '88.0');
      formData.append('rainfall_mm', '12.0');
      formData.append('leaf_wetness_hours', '11.5');

      const data = await api.diagnoseLeaf(formData);
      onDiagnosisComplete(data);
    } catch (err) {
      console.error("Diagnosis call failed:", err);
      alert("Error contacting backend model service. Make sure backend server is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 md:p-6 shadow-xs hover:shadow-md transition-shadow mb-8">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200">
          <Camera className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-900">{t.uploadTitle}</h3>
          <p className="text-xs text-slate-500">{t.uploadDesc}</p>
        </div>
      </div>

      {/* Image Dropzone & Preview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-5">
        <div className="border-2 border-dashed border-slate-300 hover:border-emerald-600 rounded-xl p-6 text-center transition-colors bg-slate-50 hover:bg-emerald-50/40 flex flex-col items-center justify-center">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            id="leaf-upload-input"
            className="hidden"
          />
          <label htmlFor="leaf-upload-input" className="cursor-pointer flex flex-col items-center">
            <Upload className="w-9 h-9 text-emerald-700 mb-2" />
            <span className="text-sm font-semibold text-slate-800">{t.chooseFile}</span>
            <span className="text-xs text-slate-500 mt-1">Supports JPG, PNG, WEBP</span>
          </label>
        </div>

        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 flex flex-col items-center justify-center relative min-h-[160px]">
          {previewUrl ? (
            <div className="relative w-full h-40 flex items-center justify-center overflow-hidden rounded-lg">
              <img src={previewUrl} alt="Leaf Preview" className="max-h-full object-contain rounded-lg shadow-xs" />
              <span className="absolute bottom-2 right-2 text-xs bg-slate-900/80 text-white px-2 py-0.5 rounded font-mono text-[10px]">
                224x224 RGB
              </span>
            </div>
          ) : (
            <div className="text-center text-slate-400">
              <ImageIcon className="w-9 h-9 mx-auto mb-1 opacity-50 text-slate-400" />
              <span className="text-xs text-slate-500">No image loaded yet</span>
            </div>
          )}
        </div>
      </div>

      {/* Quick Test Sample Images */}
      <div className="mb-5">
        <span className="text-xs font-semibold text-slate-600 block mb-2">{t.sampleTestImages}</span>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {sampleImages.map((s, idx) => (
            <button
              key={idx}
              onClick={() => handleSampleClick(s)}
              className={`px-3 py-2 text-xs font-semibold rounded-lg border transition-all text-left flex items-center justify-between ${
                selectedSample === s.filename
                  ? 'bg-emerald-100 border-emerald-500 text-emerald-900 shadow-xs'
                  : 'bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-700'
              }`}
            >
              <span>{s.label}</span>
              <Sparkles className="w-3.5 h-3.5 text-amber-600" />
            </button>
          ))}
        </div>
      </div>

      <button
        onClick={() => runDiagnosis()}
        disabled={!file || loading}
        className={`w-full py-3 px-4 rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-all shadow-xs ${
          !file || loading
            ? 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200'
            : 'bg-emerald-700 hover:bg-emerald-800 text-white font-bold shadow-xs'
        }`}
      >
        {loading ? (
          <>
            <RefreshCw className="w-4 h-4 animate-spin" />
            {t.analyzing}
          </>
        ) : (
          <>
            <CheckCircle className="w-4 h-4" />
            {t.diagnoseBtn}
          </>
        )}
      </button>
    </div>
  );
}
