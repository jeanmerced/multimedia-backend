/**
 * Vuex store for multimedias, with actions, mutations, getters and state.
 * @module multimedias
 */

//These mutations allow you to modify the state of the application.
export default{

    /**
     * Mutation to set the loaded multimedia post's data in the state.
     * @param {*} state vuex state object
     * @param {*} multimedia loaded multimedia post object with data
     */
    SET_MULTIMEDIA(state,multimedia){
        //Set multimedia post data
        state.multimedia = multimedia
    },

    /**
     * Mutation to set the loaded multimedia posts list in the state.
     * @param {*} state vuex state object
     * @param {*} multimedias loaded multimedia posts list with objects containing multimedia post data
     */

    SET_MULTIMEDIAS(state,multimedias){
        //Set loaded multimedia posts list
        state.multimedias = multimedias
    },

    /**
     * Mutation to filter the state's multimedia posts effectively deleting them.
     * @param {*} state vuex state object
     * @param {*} mid id of the multimedia post being deleted
     */
    DELETE_MULTIMEDIA(state,mid){
        state.multimedias = state.multimedias.filter(multimedias => multimedias.mid !== mid)
    },

    /**
     * Mutation to add a new multimedia post to the state's multimedia post list.
     * @param {*} state vuex state object
     * @param {*} multimedia Object with the information of the multimedia post being added.
     */
    ADD_MULTIMEDIA(state,multimedia){
        state.multimedias.push(multimedia)
    },

    /**
     * Mutation to set the information of the updated multimedia post in the state's multimedia posts list.
     * @param {*} state vuex state object
     * @param {*} multimedia multimedia post Object with the information of the multimedia post being updated
     */
    UPDATE_MULTIMEDIA(state,multimedia){
        const index = state.multimedias.findIndex(arrmultimedia => arrmultimedia.mid === multimedia.mid)
        if(index !== -1){
            //Substitute the old multimedia post with the update multimedia post
            state.multimedias.splice(index,1,multimedia)
        }
    }
}