const express=require("express")
const cors=require("cors")
const connectdb=require("./config/db")
const router=require("./router")
var cookieParser = require('cookie-parser')
require("dotenv").config()
const app=express()
app.use(cors(
    {
        origin : process.env.FRONTEND_URL,
        credentials:true 
    }
))

app.use(express.json())
app.use(cookieParser())
app.use("/api",router)



const port=8080||process.env.PORT 
connectdb().then(()=>
    {
        app.listen(port,()=>
            {
                console.log("connect to db")
                console.log("server is running")
            })
    }
)
