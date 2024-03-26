from Utilities.Config import db


def create(data):
    try:
        db.session.add(data)
        db.session.commit()
        return {"success": True, "message": "Data created successfully"}
    except Exception as e:
        db.session.rollback()
        print("erro: " + str(e))


def findById(model, idModel):
    return model.query.get(idModel)


def deleteById(model, idModel):
    try:
        modelDelete = model.query.get(idModel)
        db.session.delete(modelDelete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
