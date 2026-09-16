# CropGuard AI: Research Grounding & Technical Foundations

## 1. Lightweight Vision Architectures for On-Device Agriculture Diagnostics

For edge and low-bandwidth agricultural deployment (e.g., rural Indian farmlands with intermittent connectivity), model latency, binary size, and compute efficiency are paramount.

### Architectural Comparison
| Architecture | Params (M) | FLOPs (M) | Top-1 Accuracy (ImageNet) | Latency (CPU/Mobile) | Key Suitability for Plant Disease |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MobileNetV3-Small** | ~2.5M | ~66M | 67.4% | ~8-12 ms | **Ideal for edge deployment**; hard-swish activation & squeezed-and-excitation blocks give superior feature extraction on low-power devices. |
| **MobileNetV3-Large** | ~5.4M | ~219M | 75.2% | ~20-28 ms | Good balance when server-side API or mid-tier mobile hardware is available. |
| **EfficientNet-Lite0** | ~4.7M | ~407M | 75.1% | ~30-45 ms | High accuracy but higher memory footprint due to depthwise scaling. |
| **ShuffleNetV2 (1.0x)** | ~2.3M | ~146M | 69.4% | ~12-15 ms | Excellent memory throughput efficiency; channel shuffle operation handles fine leaf texture details well. |

**Selected Architecture for CropGuard AI:** **MobileNetV3-Small** (fine-tuned). It provides low parameter count, high CPU inference speed without GPU acceleration, and small model artifact size (< 10 MB).

---

## 2. Public Plant Disease Datasets & Field Domain Shift

### Key Datasets Surveyed
1. **PlantVillage (Hughes & Salathé, 2015)**: 54,303 laboratory-captured images across 14 crop species and 26 diseases.
2. **PlantDoc (Singh et al., 2019)**: ~2,598 field-captured images across 13 plant species and 17 classes, annotated for real-world disease detection in wild environments.
3. **Indian Agricultural Datasets (ICAR / KVK repository studies)**: Field imagery focusing on tropical/subtropical crops (Tomato, Potato, Maize, Rice, Wheat).

### Known Dataset Limitations & Domain Shift
- **Lab-Image Bias**: PlantVillage images are mostly taken under controlled studio lighting with single severed leaves against neutral gray/white backgrounds. Models trained purely on PlantVillage experience significant accuracy degradation (~30-45% drop) when deployed on real field photos with complex soil/weed backgrounds, direct sunlight glare, and overlapping leaves.
- **Background Interference**: Field imagery contains background noise (mulch, drip lines, shadow cast by neighboring plants).
- **Severity Absence**: Standard datasets provide categorical labels (e.g. `Tomato_Early_blight`) without quantifying severity (% leaf area infected). CropGuard AI addresses this by coupling CNN classification with HSV color segmentation for lesion area measurement.

---

## 3. Epidemiological Forecasting Models in Precision Agriculture

Traditional plant disease diagnosis is *reactive*—treating crops only after visible damage has occurred. CropGuard AI uses a **pre-symptomatic epidemiological forecasting engine (Stage A)** inspired by classical and modern plant epidemiology literature.

### The Van der Plank Disease Triangle Model
Plant disease outbreaks require three simultaneous factors:
1. **Susceptible Host**: Crop species and vulnerable growth stage (e.g., flowering/fruiting stages are highly susceptible to blight fungi).
2. **Virulent Pathogen**: Regional historical presence or spore dispersal patterns.
3. **Favorable Micro-Environment**: Weather conditions enabling spore germination and infection establishment.

$$\text{Outbreak Risk Index } (R_A) = f(\text{Temp}, \text{Relative Humidity}, \text{Rainfall}, \text{Leaf Wetness Duration}) \times \text{Host Susceptibility Multiplier}$$

### Empirical Micro-Meteorological Disease Models
- **Late Blight (*Phytophthora infestans*)**:
  - *Optimum Conditions*: Temperature 15°C – 22°C, Relative Humidity > 85%, Leaf Wetness Duration (LWD) > 10 hours.
  - *Epidemiological Rule*: Wallin's Disease Severity Value (DSV) model.
- **Early Blight (*Alternaria solani*)**:
  - *Optimum Conditions*: Temperature 24°C – 30°C with alternating wet and dry periods, RH > 75%.
  - *Epidemiological Rule*: P-Days (Physiological Days) combined with humidity duration.
- **Common Rust (*Puccinia sorghi*)**:
  - *Optimum Conditions*: Temperature 16°C – 24°C, high atmospheric humidity (RH > 90%), prolonged dew formation.

---

## 4. Pre-Symptomatic & Spectral Innovations in Crop Protection

Recent research (2024–2026) highlights advanced pre-symptomatic detection techniques:
- **Hyperspectral Imaging (HSI)**: Measures narrow spectral bands (400-1000 nm). Pre-symptomatic fungal infection alters cell wall structure and chlorophyll fluorescence (NDVI drops) 48-72 hours before visible necrotic lesions form.
- **Multispectral Satellite & Drone Imagery**: High-resolution multispectral sensors (Green, Red, Red Edge, Near-Infrared) compute canopy stress indices (NDRE, SAVI) to detect early spot infections across whole fields.
- **Micro-Climate Sensor Networks**: Combining cheap IoT leaf wetness sensors and canopy micro-weather stations with regional weather forecasts enables precision risk alerting down to the village level.

---

## 5. References & Academic Citations

1. Van der Plank, J. E. (1963). *Plant Diseases: Epidemics and Control*. Academic Press, New York.
2. Howard, A., et al. (2019). "Searching for MobileNetV3." *IEEE/CVF International Conference on Computer Vision (ICCV)*, pp. 1314-1324.
3. Hughes, D. P., & Salathé, M. (2015). "An open access repository of plant diseased leaves images for crop disease detection." *arXiv preprint arXiv:1511.08060*.
4. Singh, D., et al. (2019). "PlantDoc: A Dataset for Visual Plant Disease Detection." *Proceedings of the 7th ACM IKDD CoDS and 25th COMAD*, pp. 249-253.
5. Wallin, J. R. (1962). "Summary of recent progress in predicting late blight weather in Iowa." *Plant Disease Reporter*, 46: 766-770.
6. ICAR-Indian Agricultural Research Institute (2023). *Integrated Pest and Disease Management Guidelines for Solanaceous and Cereal Crops*. New Delhi, India.
