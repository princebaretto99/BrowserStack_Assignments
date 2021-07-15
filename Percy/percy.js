const { Builder } = require("selenium-webdriver");
const percySnapshot = require('@percy/selenium-webdriver');
const { Options } = require("selenium-webdriver/chrome");

const baseUrl = process.env.PERCY_BRANCH == "production" ? "https://www.browserstack.com" : " https://k8s.bsstag.com"
const endPoints = {
    "Index Route":"/",
    "Pricing Route":"/pricing",
    "Integration_Automate Route":"/integrations/automate",
    "Docs":"/docs"
    }

const widths_per = [375, 480, 720, 1280, 1440, 1920]

OPTIONS = {
    snapshot: {
        widths : widths_per
    }
}

async function percy_run(){
    let driver = await new Builder().forBrowser('chrome').build();
    try{
        for(let endPoint in endPoints){
            await driver.get(baseUrl + endPoints[endPoint]);
            await percySnapshot(driver,endPoint, OPTIONS);
        }
    }
    finally{
        await driver.quit();
    }
    
}
//PERCY_BRANCH=staging PERCY_TARGET_BRANCH=production percy exec -- node percy.js
percy_run();
