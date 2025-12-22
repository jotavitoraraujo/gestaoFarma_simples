### --- IMPORTS --- ###

#######################
class QuarantinePayload:
    def __init__(self, product_id: int, batch_id: int, reason: str, emitter_cnpj: str, emitter_name: str):
        self.product_id = product_id
        self.batch_id = batch_id
        self.reason = reason
        self.emitter_cnpj = emitter_cnpj
        self.emitter_name = emitter_name
    
    def to_dict(self) -> dict:
        class_dict: dict = self.__dict__
        return class_dict

class SalesDeviationPayload: # -> REFATORAR E INCLUIR ATRIBUTOS COMO USER, PRODUCT IDS (SE NECESSÁRIO)
    def __init__(self, user_id: int, order_id: int, sold_batch_id: int, correct_batch_id: int):
        self.user_id = user_id
        self.order_id = order_id
        self.sold_batch_id = sold_batch_id
        self.correct_batch_id = correct_batch_id

    def to_dict(self) -> dict:
        class_dict: dict = self.__dict__
        return class_dict
    
class ImportationFinishedPayload:
    def __init__(self, status: str, file_name: str, total_records: int):
        self.status = status
        self.file = file_name
        self.total_records = total_records

    def to_dict(self) -> dict:
        class_dict: dict = self.__dict__
        return class_dict