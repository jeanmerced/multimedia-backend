/**
 * Vuex store for multimedias, with actions, mutations, getters and state.
 * @module multimedias
 */

export default {

    /**
     * Action to fetch all multimedia posts from the database
     * @param {*} param0  destructuring of vuex context object
     */
    async getMultimedias({ commit, dispatch }) {
        try {

            const response = await this.$axios.get('multimedia')
            commit("SET_MULTIMEDIAS", response.data.Multimedias)


        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
                
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})                

            }
        }
    },

    /**
     * Action to fetch multimedia posts by their author dashboard user id from the database.
     * @param {*} param0 destructuring of vuex context object
     * @param {*} duid dashboard user id of the author of the multimedia posts being fetched
     */
    async getMultimediasByAuthor({ commit, dispatch }, duid) {
        try {
            const response = await this.$axios.get('multimedia/' + duid)
            commit("SET_MULTIMEDIAS", response.data.Multimedias)

        } catch (error) {
            if (!!error.response.data) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
                return 'error'

            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})

            } 
        }
    },

    /**
     * Action to fetch multimedia post by their type from the database.
     * @param {*} param0 destructuring of vuex context object
     * @param {*} type type of the multimedia posts being fetched
     */
    async getMultimediasByType({ commit, dispatch }, type) {
        try {
            const response = await this.$axios.get('multimedia/' + type)
            commit("SET_MULTIMEDIAS", response.data.Multimedias)

        } catch (error) {
            if (!!error.response.data) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
                return 'error'

            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})

            } 
        }
    },

    /**
     * Action to add a new multimedia post to the system given the information
     * in the multimedia post creation form
     * @param {*} param0 destructuring of vuex context object
     * @param {*} multimediaJSON Object containing the information of the multimedia post to be added.
     */
    async addMultimedia({ commit, dispatch }, multimediaJSON) {
        try {
            const response = await this.$axios.post('multimedia', multimediaJSON)
            commit("ADD_MULTIMEDIA", response.data.Multimedia)
            dispatch('notifications/setSnackbar', { text: "Se añadió una nueva publicación multimedia exitosamente", color: 'success' }, { root: true })

        } catch (error) {
            if (!!error.response.data) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
                return 'error'
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
        }
    },

    /**
     * Action to edit a multimedia post's information by their id and information given
     * in the multimedia post edit form.
     * @param {*} param0 destructuring of vuex context object
     * @param {*} multimediaJSON Object containing the information of the multimedia post to be edited.
     */
    async editMultimedia({ commit, dispatch }, multimediaJSON) {
        try {

            const response = await this.$axios.put('multimedia/' + multimediaJSON.mid, multimediaJSON)
            commit("UPDATE_MULTIMEDIA", response.data.Multimedia)
            dispatch('notifications/setSnackbar', { text: `La publicación multimedia con identificador:${multimediaJSON.mid} ha sido editada.`, color: 'success' }, { root: true })

        } catch (error) {
            console.log(error)
            if (!!error.response.data) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
                'return error'
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
        }
    },

    /**
     * Action to remove a multimedia post from the system given their id.
     * @param {*} param0 destructuring of vuex context object
     * @param {*} mid id of the multimedia post being removed
     */
    async removeMultimedia({ commit, dispatch }, mid) {
        try {

            const response = await this.$axios.delete('multimedia/' + mid)
            commit("DELETE_MULTIMEDIA", mid)
            dispatch('notifications/setSnackbar', { text: response.data.Multimedia, color: 'success' }, { root: true })

        } catch (error) {
            if (!!error.response.data) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
                return 'error'
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
        }
    },
}

