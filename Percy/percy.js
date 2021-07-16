const { Builder } = require("selenium-webdriver");
const percySnapshot = require('@percy/selenium-webdriver');
const { Options } = require("selenium-webdriver/chrome");
// const dotenv = require('dotenv');
// dotenv.config();

const baseUrl = process.env.PERCY_BRANCH == "production" ? "https://www.browserstack.com" : "https://k8s.bsstag.com"

const endPoints = {
    "Index Route":"/",
    "Pricing Route":"/pricing",
    "Integration_Automate Route":"/integrations/automate",
    "Docs":"/docs"
    }

async function percy_run(){
    let driver = await new Builder().forBrowser('chrome').build();
    try{
        for(let endPoint in endPoints){
            await driver.get(baseUrl + endPoints[endPoint]);
            await percySnapshot(driver,endPoint);
        }
    }
    finally{
        await driver.quit();
    }
    
}
//PERCY_BRANCH=staging PERCY_TARGET_BRANCH=production percy exec --config ./config/percy.conf.yml -- node percy.js
//PERCY_BRANCH=production percy exec --config ./config/percy.conf.yml -- node percy.js
percy_run();
