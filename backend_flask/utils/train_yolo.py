from ultralytics import YOLO


if __name__ == '__main__':

    model=YOLO("yolov8n.pt")

    results=model.train(data="ocr_91percent.yaml",
                        epochs=50,
                        batch=16,
                        imgsz=1024,
                        single_cls=True,
                        name="ocr_91percent")