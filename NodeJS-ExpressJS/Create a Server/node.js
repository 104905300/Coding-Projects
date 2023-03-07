const os = require("os")
const {writeFile} = require("fs").promises

console.log(`Hello ${os.uptime()} World!`)

const start = async () => { // note this is only a decleartion of function, it does not invoke it until the line start()
    try {
        // with await you don't need to have a callback function as your third parameter, e.g. writeFile("./testing.txt", "I LOVE YOU!", (err,result) => {})
        await writeFile("./testing.txt", "I LOVE YOU!")
        await writeFile("./testing2.txt", "I LOVE YOU TOO!")
    } catch (error) { 
        // writeFile return a promise object (from require("fs").promises), await works on promise object, and will either run reolve() or reject()
        // if reject() is run it will be caught here as an error 
        console.log(`There is an error! Here is the error message: ${error}`)
    }
}

start()


//comment

