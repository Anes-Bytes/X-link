class SubdomainAvailabilitySerializer:
    @staticmethod
    def serialize(result):
        return {
            "available": result.available,
            "reason": result.reason,
        }
