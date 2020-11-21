from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2

class MultimediaDAO:

    def __init__(self):
        #Extract relational database credentials.
        connection_url = "dbname={} user={} password={} host={} ".format(
        db_config['database'],
        db_config['username'],
        db_config['password'],
        db_config['host']
        )
        
        #Establish a connection with the relational database.
        self.conn = psycopg2.connect(connection_url) 

    def addMultimedia(self, title, content, mType, duid):
        """
        Summary:
            Creates a multimedia post with the given title, content, type of multimedia, and author,
            and inserts it into the database returning the id of the newly created multimedia post if succesful,
            or an error if otherwise.

        Params:
            title: the title of the multimedia post.
            content: the content of the post.
            mType: the type of multimedia post.
            duid: the dashboard user id of the author of the multimedia post.

        Returns:
            The id of the newly added multimedia post
        """
        cursor = self.conn.cursor() 

        query = "insert into multimedia (title, content, type, date_published, is_invalid, duid)"\
                "values (%s, %s, %s, current_timestamp, false, %s) returning mid;"

        mID = None
        
        try:
            cursor.execute(query, (title, content, mType, duid,))       
            mID = cursor.fetchone()[0]
            cursor.close()
            if not mID:
                return "Occurrió un error interno tratando de añadir una publicación multimedia."       
        except psycopg2.DatabaseError as e:
            print(e)
            return "Occurrió un error interno tratando de añadir una publicación multimedia."
        
        #Commits the changes done on the database after insertion
        try:
            self._commitChanges()                   
        except:
            return "Occurrió un error interno tratando de añadir una publicación multimedia."
        
        #Return id of the newly created multimedia post
        return mID

    def getAllMultimedia(self):
        """
        Summary:
            Returns a list of all multimedia posts that are valid in the database with their corresponding information.

        Returns:
            A list containing all the valid multimedia posts with their information.
        """

        cursor = self.conn.cursor()

        query = """select mid, title, content, type, date_published
                   from multimedia
                   where is_invalid = false
                """
        
        result = []
        
        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row)
            return result
        except psycopg2.DatabaseError as e:
            print(e)
            return "Ocurrió un error interno buscando todas las publicaciones multimedia."

    def getMultimediaByID(self, mID):
        """
        Summary:
            Returns a single multimedia post that is valid in the database with their corresponding information
            with the given multimedia post id.

        Params:
            mID: the id of the multimedia post id to be fetched.

        Returns:
            A list containing all the information of the valid multimedia post with the given multimedia post id.
        """
        
        cursor = self.conn.cursor()
        
        query = """select mid, title, content, type, date_published
                   from multimedia
                   where mid = %s
                   and is_invalid = false
                """
        
        try:
            cursor.execute(query,(mID,))
            result = cursor.fetchone()
            return result
        except psycopg2.DatabaseError as e:
            print(e)
            return "Ocurrió un error interno buscando una publicación multimedia por su identificador."
    
    def getMultimediaByType(self, mType):
        """
        Summary:
            Returns a a list of multimedia posts that are valid in the database with their corresponding information
            and are of the given type.

        Params:
            mType: the type of multimedia post.

        Returns:
            A list containing all the valid multimedia posts with their information and are of the given type.
        """

        cursor = self.conn.cursor()

        query = """select mid, title, content, type, date_published
                   from multimedia
                   where type = %s
                   and is_invalid = false
                """

        result = []
        
        try:
            cursor.execute(query, (mType,))
            for row in cursor:
                result.append(row)
            return result
        except psycopg2.DatabaseError as e:
            print(e)
            return "Occurrió un error interno buscando publicaciones del tipo de multimedia dado."

    def getMultimediaByAuthor(self, duid):
        """
        Summary:
            Returns a a list of multimedia posts that are valid in the database with their corresponding information
            and are authored by the dashboard user with the given id.

        Params:
            duid: the dashboard user id of the author of the multimedia post.

        Returns:
            A list containing all the valid multimedia posts with their information and are authored by the dashboard 
            user with the given id.
        """

        cursor = self.conn.cursor()
        
        query = """select mid, title, content, type, date_published
                   from multimedia as M inner join dashboard_user as DU on M.duid=DU.id
                   where DU.id = %s 
                   and M.is_invalid = false
                """
        
        result = []
        
        try:
            cursor.execute(query, (duid,))
            for row in cursor:
                result.append(row)
            return result
        except psycopg2.DatabaseError as e:
            print(e)
            return "Occurrió un error interno buscando publicaciones de multimedia del autor dado." 

    def editMultimedia(self, mID, title, content):
        """
        Summary:
            Updates an existing multimedia post in the database using the given title, content, type of multimedia, 
            and author, returning the id of the newly updated multimedia post if succesful, or an error if otherwise.

        Params:
            mID: the id of the multimedia post to be updated.
            title: the title of the multimedia post.
            content: the content of the post.
            mType: the type of multimedia post.
            duid: the dashboard user id of the author of the multimedia post.

        Returns:
            The id of the newly updated multimedia post.
        """

        cursor = self.conn.cursor()
        
        query = """update multimedia
                   set title = %s,
                       content = %s
                   where mid = %s
                   returning mid
                """
        
        result = None
        
        try:
            cursor.execute(query,(title, content, mID,))
            result = cursor.fetchone()
            if not result:
                return "Occurrió un error interno editando una publicación multimedia existente."
        except Exception as e:
            print(e)
            return "Ocurrió un error interno editando una publicación multimedia existente."             
        
        try:
            self._commitChanges()                  
        except:
            return "Ocurrió un error interno editando una publicación multimedia existente."            
       
        #Return id of the newly updated multimedia post
        return result[0] 
    
    def removeMultimedia(self, mID):
        """
        Summary:
            Sets as invalid a multimedia post in the database with the given multimedia post id.
            This effectively acts as a removal of the multimedia post from the system.

        Params:
            mID: The id of the multimedia post to invalidate.

        Returns:
            The id of the updated and invalid multimedia post.
        """
        
        cursor = self.conn.cursor()
        
        query = """update multimedia
                   set is_invalid = true
                   where mid = %s
                   returning mid;
                """
        
        result = None
        
        try:
            cursor.execute(query, (mID, ))
            result = cursor.fetchone()
            if not result:
                return "Occurrió un error interno removiendo una publicación multimedia existente."
        except Exception as e:
            print(e)
            return "Ocurrió un error interno removiendo una publicación multimedia existente."             
        
        try:
            self._commitChanges()                  
        except:
            return "Ocurrió un error interno removiendo una publicación multimedia existente."  

        #Return id of the newly updated multimedia post
        return result[0] 

    def multimediaExists(self, mID):
        """
        Summary:
            Confirms the existence of a multimedia post in the database by the multimedia post id given.

        Params:
            mID: the id of the multimedia post in question.

        Returns:
            True if the multimedia post exists, false otherwise.
        """
        
        cursor = self.conn.cursor()
        
        exists = True
        
        query = """select mID
                   from multimedia
                   where mID = %s
                   and is_invalid = false
                """
        try:
            cursor.execute(query,(mID,))
            if not cursor.fetchone():
                exists = False
        except Exception as e:
            print(e)
            exists = False
        
        return exists

    def _commitChanges(self):
        """
        Summary:
            Commits the changes done on the database after
            insertion and update queries.
        """
        self.conn.commit()

    def _closeConnection(self):
        """
        Summary:
            Closes the connection with the database.
        """
        if self.conn is not None:
            self.conn.close()