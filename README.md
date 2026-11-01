# Spacecraft Telemetry Anomaly Detector
A full-stack machine learning and data engineering pipeline designed to ingest multi-channel NASA time-series telemetry data, process it through a Python and PostgreSQL backend, train a custom PyTorch neural network anomaly detector, and expose system performance and logging via an interactive terminal interface made with ReactJS and a Spring Boot backend.

# Tech Stack
- **Languages:** Python, Java, JavaScript
- **Dataset:** [Kaggle](https://www.kaggle.com/datasets/patrickfleith/nasa-anomaly-detection-dataset-smap-msl/data)
- **Database:** PostgreSQL
- **Libraries:** PyTorch, NumPy, Pandas, Matplotlib
- **Frameworks:** Spring Boot
- **IDE:** Visual Studio Code

# Features
- **Neural Network:** Implements a PyTorch Multi-Layer Perceptron to predict next telemetry value in a sliding window sequence and utilizes Mean Squared Error scoring to flag anomalies.
- **Data Pipeline:** Parsed binary files, prepared sliding-window tensors, and mapped time-series. Integrated PostgreSQL for data logging.
- **Data Visualization:** Created graphs with Matplotlib to visualize training and validation learning curves of the network.
- **Backend & API Layer:** Coordinates data flow, business logic, and API integration with Spring Boot.
- **Frontend & User Interface**: Works with Spring Boot backend to visually display project information on a GUI made with ReactJS.

# Future Works / Improvements
- **Parameterization:** Hardcoding certain features/variables caused issues along the way as more channels were trained and tested.
- **Better Preparation When Working w/ Datasets:** Assumptions about how the dataset was structured caused dimensional issues. Examples being assuming each channel had the same dimensions of data and each channel was going to be trained/evaluated with hardcoded settings.
- **More Advanced Neural Network Model:** Given that a Multi-Layer Perceptron was as basic as Neural Networks get, this model was temporally blind with no contextual awareness, which caused issues as some channels heavily depended on context and a sliding-window was not sufficient enough to capture that.
- **More Meaningful Interface:** The current GUI played a purpose of mainly showcasing backend to frontend integration using Spring Boot, ReactJS, and APIs.

# (Video Demo)[https://drive.google.com/file/d/17KQtQFrJzHzLbHhu1LbJY5lxobmSKyBs/view?usp=sharing]

# Date
October 2026
