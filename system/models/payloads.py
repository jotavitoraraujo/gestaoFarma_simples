### --- IMPORTS --- ###

#######################
class QuarantinePayLoad:
    def __init__(self, batch_id: int, reason: str, emitter_cnpj: str, emitter_name: str):
        self.batch_id = batch_id
        self.reason = reason
        self.emitter_cnpj = emitter_cnpj
        self.emitter_name = emitter_name
    
    def to_dict(self) -> dict:
        class_dict: dict = self.__dict__
        return class_dict

class SalesDeviationPayload:
    def __init__(self, user_id: int, order_id: int, sold_batch_id: int, correct_batch_id: int):
        self.user_id = user_id
        self.order_id = order_id
        self.sold_batch_id = sold_batch_id
        self.correct_batch_id = correct_batch_id

    def to_dict(self) -> dict:
        class_dict: dict = self.__dict__
        return class_dict