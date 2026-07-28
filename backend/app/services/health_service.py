class HealthService:
    @staticmethod
    def get_health_status():
        return {
            "status": "healthy",
            "service": "AgriSahayak AI",
            "version": "1.0.0"
        }