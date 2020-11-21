from flask import jsonify
from .dao.multimedia_dao import MultimediaDAO
from .dao.user_dao import UserDAO

class MultimediaHandler:
    
    def mapMultimediaToDict(self, record):
        """
        Summary:
            Converts a multimedia post record returned by the MultimediaDAO into a dictionary and returns it.

        Params:
            record: a multimedia post record in the database with its information.
        
        Returns:
            A dictionay containing the multimedia post information given in the record.
        """

        result = {}
        result['mid'] = record[0]
        result['title'] = record[1]
        result['content'] = record[2]
        result['type'] = record[3]
        result['date_published'] = record[4]
        
        return result

    def addMultimedia(self, attributes):
        """
        Summary:
            Adds a new multimedia post with the information given and maps the result to a JSON object that 
            contains the information of the newly added multimedia post
        
        Params:
            attributes: a dictionary containing the attributes of the multimedia post to be added.
        
        Returns:
            A JSON object containing the information of the newly added multimedia post.
        """
        
        #Validate request json attributes comply with the system specifications
        validationResult = self._validateInsertAttributes(attributes)
        if isinstance(validationResult, str):
            return jsonify(Error = validationResult), 400

        dao = MultimediaDAO()

        try:
            #Add multimedia post using DAO
            result = dao.addMultimedia(attributes['title'], attributes['content'], attributes['type'], attributes['duid'])

            #Fetch newly created multimedia post by its id to return
            multimedia = dao.getMultimediaByID(result)
            dao._closeConnection()

            #Convert multimedia post record into a dictionary
            mappedResult = self.mapMultimediaToDict(multimedia)
            return jsonify(Multimedia = mappedResult), 201
        except Exception as e:
            print(e)
            dao._closeConnection()
            return jsonify(Error = "Ocurrió un error interno tratando de añadir una nueva publicación multimedia."), 500

    def getAllMultimedia(self):
        """
        Summary:
            Gets a list of all multimedia posts that are valid in the database and maps the result to a JSON
            object containing all the valid multimedia posts and their information. The JSON objects is then 
            returned or an error if otherwise. 

        Returns:
            A JSON object containing all valid multimedia posts and their information.
        """
    
        dao = MultimediaDAO()
        
        try:
            #Get all multimedia posts using DAO
            result = dao.getAllMultimedia()
            dao._closeConnection()
            if not result:
                return jsonify(Error = "Ninguna publicación multimedia fue encontrada."), 404

            #Convert multimedia post records into a list of dictionaries
            mappedResult = []
            for multimedia in result:
                mappedResult.append(self.mapMultimediaToDict(multimedia))
            return jsonify(Multimedias = mappedResult), 200
        except Exception as e:
            print(e)
            dao._closeConnection()
            return jsonify(Error = "Ocurrió un error interno buscando todas las publicaciones multimedia."), 500

    def getMultimediaByID(self, mID):
        """
        Summary:
            Gets a single multimedia post specified by the given multimedia post id that is valid in the 
            database and maps the result to a JSON object containing its information. The JSON objects is 
            then returned or an error if otherwise. 

        Params:
            mID: the id of the multimedia post id to be fetched.

        Returns:
            A JSON object containing all the information of the valid multimedia post with the given multimedia post id.
        """

        #Validate multimedia post id is an intenger greater than 0
        if not isinstance(mID, int) or mID < 1:
            return jsonify(Error = "El identificador de la publicación multimedia no es válido."), 400
        
        dao = MultimediaDAO()
        
        try:
            #Check if multimedia post with given id exists
            if not dao.multimediaExists(mID):
                dao._closeConnection()
                return jsonify(Error = "No existe una publicación multimedia con el identificador: {}".format(mID)), 404

            #Get multimedia post given its id using DAO
            multimedia = dao.getMultimediaByID(mID)
            dao._closeConnection()

            #Convert multimedia post record into a dictionary
            mappedResult = self.mapMultimediaToDict(multimedia)
            return jsonify(Multimedia = mappedResult), 200
        except Exception as e:
            print(e)
            dao._closeConnection()
            return jsonify(Error = "Ocurrió un error interno buscando una publicación multimedia por su identificador."), 500

    def getMultimediaByType(self, mType):
        """
        Summary:
            Gets a list of multimedia posts specified by the given multimedia type that are valid in the 
            database and maps the result to a JSON object containing its information. The JSON objects is 
            then returned or an error if otherwise. 

        Params:
            mType: the type of the multimedia post to be fetched.

        Returns:
            A JSON object containing all valid multimedia posts and their information of the given type.        
        """

        #Validate that the type of multimedia exists
        if not (mType == 'text' or mType == 'image' or mType == 'video' or mType == 'livestream'): 
            return jsonify(Error = "El identificador del tipo de multimedia dado no es válido."), 400
        
        dao = MultimediaDAO()
        
        try:  
            #Get multimedia post given its type using DAO
            result = dao.getMultimediaByType(mType) 
            dao._closeConnection()
            if not result:
                return jsonify(Error = "Ninguna publicación del tipo de multimedia dado fue encontrada."), 404

            #Convert multimedia post records of the given type into a list of dictionaries
            mappedResult = []
            for multimedia in result:
                mappedResult.append(self.mapMultimediaToDict(multimedia))
            return jsonify(Multimedias = mappedResult), 200        
        except Exception as e:
            print(e)
            dao._closeConnection()
            return jsonify(Error = "Occurrió un error interno buscando publicaciones del tipo de multimedia dado."), 500

    def getMultimediaByAuthor(self, duid):
        """
        Summary:
            Gets a list of multimedia posts authored by the dashboard user with the given id that are valid in the 
            database and maps the result to a JSON object containing its information. The JSON objects is 
            then returned or an error if otherwise. 

        Params:
            duid: the dashboard user id of the author of the multimedia posts to be fetched.

        Returns:
            A JSON object containing all valid multimedia posts and their information authored by the dashboard user with the given id.        
        """

        user_dao = UserDAO()
        dao = MultimediaDAO()
        
        try:
            #Check dashboard user with given id exists
            if not user_dao.getDashUserByID(duid):
                return jsonify(Error = "El identificador del autor de la publicación multimedia dado no es válido."), 400

            #Get multimedia posts by author using DAO
            result = dao.getMultimediaByAuthor(duid) 
            dao._closeConnection()
            if not result:
                return jsonify(Error = "Ninguna publicación multimedia del autor dado fue encontrada."), 404

            #Convert multimedia post records of the given author into a list of dictionaries
            mappedResult = []
            for multimedia in result:
                mappedResult.append(self.mapMultimediaToDict(multimedia))
            return jsonify(Multimedias = mappedResult), 200        
        except Exception as e:
            print(e)
            dao._closeConnection()
            return jsonify(Error = "Occurrió un error interno buscando publicaciones de multimedia del autor dado."), 500

    def editMultimedia(self, mID, attributes):
        """
        Summary:
            Edits the attributes of an existing multimedia post that is valid in the database with the given 
            multimedia post id and maps the result to a JSON object that contains the information of the newly
            updated multimedia post
        
        Params:
            mID: the id of the multimedia post to be edited.
            attributes: a dictionary containing the attributes of the multimedia post to be edited.
        
        Returns:
            A JSON object containing the information of the edited multimedia post.
        """
        
        #Validate multimedia post id is an intenger greater than 0
        if not isinstance(mID, int) or mID < 1:
            return jsonify(Error = "El identificador de la publicación multimedia dado no es válido."), 400

        #Validate request json attributes comply with the system specifications
        validationResult = self._validateUpdateAttributes(attributes)
        if isinstance(validationResult, str):
            return jsonify(Error = validationResult), 400

        dao = MultimediaDAO()
        
        try:
            #Check if multimedia post with given id exists
            if not dao.multimediaExists(mID):
                dao._closeConnection()
                return jsonify(Error = "No existe una publicación multimedia con identificador: {}".format(mID)), 404

            #Edit multimedia post using DAO
            result = dao.editMultimedia(mID, attributes['title'], attributes['content'])

            #Fetch newly updated multimedia post by its id to return
            multimedia = dao.getMultimediaByID(result)
            dao._closeConnection()

            #Convert multimedia post record into a dictionary
            mappedResult = self.mapMultimediaToDict(multimedia)
            return jsonify(Multimedia = mappedResult), 200
        except Exception as e:
            print(e)
            dao._closeConnection()
            return jsonify(Error = "Ocurrió un error interno editando una publicación multimedia existente."), 500
    
    def removeMultimedia(self, mID):
        """
        Summary:
            Invalidates in the database a multimedia post with the given multimedia post id.
            This effectively acts as a removal of the multimedia post from the system.
        
        Params:
            mID: the id of the multimedia post to invalidate.
        
        Returns:
            A JSON object containing the id of the updated and invalid multimedia post.
        """
        
        #Validate multimedia post id is an intenger greater than 0
        if not isinstance(mID, int) or mID < 1:
            return jsonify(Error = "El identificador de la publicación multimedia dado no es válido."), 400

        dao = MultimediaDAO()
        
        try:
            #Check if multimedia post with given id exists
            if not dao.multimediaExists(mID):
                dao._closeConnection()
                return jsonify(Error = "No existe una publicación multimedia con identificador: {}".format(mID)), 404

            #Remove multimedia post using DAO
            result = dao.removeMultimedia(mID)
            dao._closeConnection()
            if not result:
                return jsonify(Error = "Occurrió un error interno removiendo una publicación multimedia existente"), 500
            return jsonify(Multimedia = "Se removió la publicación multimedia con identificador: {}".format(result)), 200
        except Exception as e:
            print(e)
            dao._closeConnection()
            return jsonify(Error = "Ocurrió un error interno removiendo una publicación multimedia existente"), 500

    def _validateInsertAttributes(self,attributes):
        """
        Summary:
            Validates the attributes dictionary given to add a multimedia post.

        Params:
            attributes: a dictionary containing the attributes of the multimedia post to be added.
        
        Returns:
            A string with an error message if the validation fails an integer otherwise.        
        """
        
        #Validate that attributes is a dictionary
        if not isinstance(attributes, dict):
            return "Los attributos dados no son válidos."       
        
        try:
            title = attributes['title']
            content = attributes['content']
            mType = attributes['type']
            duid = attributes['duid']
   
            #Title must be string with maximum length of 300 characters
            if not title or not isinstance(title, str) or len(title) > 300:
                return "El título dado no es válido."

            #Content must be string with maximum length of 63206 characters
            if not content or not isinstance(content, str) or len(content) > 63206:
                return "El contenido dado no es válido."

            #Type can take the value of: text, image, video, or livestream. 
            if not mType or not (mType == 'text' or mType == 'image' or mType == 'video' or mType == 'livestream'): 
                print(mType)
               
                return "El identificador del tipo de multimedia dado no es válido."

            #Dashboard user id must be an integer greater than 0 and must correspond to a user    
            if not duid or not isinstance(duid, int) or duid < 1 or not UserDAO().getDashUserByID(duid):
                return "El identificador del autor de la publicación dado no es válido."
        except Exception as e:
            print(e)
            return "Los argumentos dados no son válidos." 
        
        #If succesful return 1
        return 1  

    def _validateUpdateAttributes(self,attributes):
        """
        Summary:
            Validates the attributes dictionary given to edit a multimedia post.

        Params:
            attributes: a dictionary containing the attributes of the multimedia post to be edited.
        
        Returns:
            A string with an error message if the validation fails an integer otherwise.        
        """
        
        #Validate that attributes is a dictionary
        if not isinstance(attributes, dict):
            return "Los attributos dados no son válidos."       
        
        try:
            title = attributes['title']
            content = attributes['content']
   
            #Title must be string with maximum length of 300 characters
            if not title or not isinstance(title, str) or len(title) > 300:
                return "El título dado no es válido."

            #Content must be string with maximum length of 63206 characters
            if not content or not isinstance(content, str) or len(content) > 63206:
                return "El contenido dado no es válido."

        except Exception as e:
            print(e)
            return "Los argumentos dados no son válidos." 
        
        #If succesful return 1
        return 1  