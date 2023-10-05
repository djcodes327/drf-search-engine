const loginForm = document.getElementById('login-form')
const searchForm = document.getElementById('search-form')
const contentContainer = document.getElementById('content-container')
const baseEndPoint = "http://localhost:8000/api"
console.log("Inside Client")
if (loginForm) {
    // Handle this login form
    loginForm.addEventListener('submit', handleLogin)
}

if (searchForm) {
    // Handle this login form
    searchForm.addEventListener('submit', handleSearch)
}

function handleSearch() {
    event.preventDefault()

    let searchFormData = new FormData(searchForm)
    let data = Object.fromEntries(searchFormData)
    let searchParams = new URLSearchParams(data)
    const searchEndPoint = `${baseEndPoint}/search/?${searchParams}`
    const headers = {
        "Content-Type": "application/json",
    }
    const getToken = localStorage.getItem("access")
    if (getToken) {
        headers["Authorization"] = `Bearer ${getToken}`
    }

    const options = {
        method: "GET",
        headers: headers,
    }
    fetch(searchEndPoint, options)
        .then(response => {
            return response.json()
        })
        .then(data => {
            const validData = isTokenValid(data)
            if (validData && contentContainer) {
                contentContainer.innerHTML = ""
                if (data && data.hits) {
                    let htmlstr = ""
                    for (let result of data.hits) {
                        htmlstr += "<li>" + result.title + "</li>"
                    }
                    contentContainer.innerHTML = htmlstr
                    if (data.hits.length === 0) {
                        contentContainer.innerHTML = "<p> No Results found </p>"
                    }
                }
            } else {
                contentContainer.innerHTML = "<p> No Results found </p>"
            }
        })
        .catch(err => {
            console.log("err", err)
        })
}

function handleLogin(event) {
    console.log(event)
    event.preventDefault()
    const loginEndPoint = `${baseEndPoint}/token/`
    let loginFormData = new FormData(loginForm)
    let loginObjectData = Object.fromEntries(loginFormData)
    console.log("Login Object Data : ", loginObjectData)
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(loginObjectData)
    }
    fetch(loginEndPoint, options)
        .then(response => {
            console.log(response)
            return response.json()
        })
        .then(authData => {
            handleAuthData(authData, getProductList)
        })
        .catch(err => {
            console.log("err", err)
        })
}

function handleAuthData(authData, callback) {
    localStorage.setItem("access", authData.access)
    localStorage.setItem("refresh", authData.refresh)
    if (callback) {
        callback()
    }
}

function writeToContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>"
    }
}

function getFetchOptions(method, body) {
    return {
        method: method === null ? "GET" : method,
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("access")}`
        },
        body: body ? body : null
    }
}

function isTokenValid(jsonData) {
    if (jsonData && jsonData.code === "token_not_valid") {
        alert("Please Login again")
        return false
    }
    return true
}

function validateJWTToken() {
    const endpoint = `${baseEndPoint}/token/verify/`
    let body = JSON.stringify({
        token: localStorage.getItem("access")
    })
    const options = getFetchOptions("POST", body)
    fetch(endpoint, options)
        .then(response => {
            return response.json()
        })
        .then(data => {
            console.log(data)
            isTokenValid(data)
        })
}

function getProductList() {
    const endpoint = `${baseEndPoint}/products/`
    const options = getFetchOptions()
    fetch(endpoint, options)
        .then(response => {
            return response.json()
        })
        .then(data => {
            const validData = isTokenValid(data)
            if (validData) {
                writeToContainer(data)
            }
        })
}

validateJWTToken()
// getProductList()

const searchClient = algoliasearch('JWU7AAZRFO', 'dc711718e6d9dfa535bd9bdfb9f90c79');

const search = instantsearch({
    indexName: 'dj_Product',
    searchClient,
});

search.addWidgets([
    instantsearch.widgets.searchBox({
        container: '#searchbox',
    }),

    instantsearch.widgets.refinementList({
        container: '#user-list',
        attribute: 'user'
    }),

    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            item: `<div> {{ title }} <p> \${{ price }}</p> </div>`
        }
    })
]);

search.start();

