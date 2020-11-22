/**
 * Vuex store for multimedias, with actions, mutations, getters and state.
 * @module multimedias
 */

export default() =>({
    /**
     * Loaded multimedia post
     */
    multimedia: null, //Used in the single multimedia post viewer page.
    /**
     * List of all multimedia posts.
     */
    multimedias: [],//Used in in the all multimedia posts viewer page.
})