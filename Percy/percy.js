const { Builder } = require("selenium-webdriver");
const percySnapshot = require('@percy/selenium-webdriver');

const baseUrl = process.env.PERCY_BRANCH == "production" ? "https://www.browserstack.com" : " https://k8s.bsstag.com"
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

percy_run();
