1. 需使用**Python3**
2. 資料夾/檔案說明：
	* **python資料夾：**
		為Python讀取「內政部不動產時價登錄網」下載下來的檔案並使用pandas實作範例程式，其中/python/plvr_land_data/下為內政部不動產時價登錄網中下載下來的csv資料，程式執行完成後會產生兩個csv檔。
	* **mongoDB資料夾：**
		為Python爬蟲591租屋網資料後，將資料存入mongoDB後，使用flask撰寫API查詢資料的程式放置位置。
	* **requirements.txt：**
		執行此專案程式需安裝的套件。
	* **網路爬蟲.pptx：**
		此專案說明ppt。
3. 安裝套件
    `pip install -r requirements.txt`
4. 執行python資料夾程式，執行程式步驟：
	1) `cd python`
	2) `python main.py`，執行完成後會產生兩的csv檔案。
5. 執行mongoDB資料夾程式，執行程式步驟：
	1) `cd mongoDB`
	2) 編輯設定檔config.ini，修改DB連線與發API的headers資訊。
	3) `python main.py`，將591租屋網上的資料存入MongoDB。
	4) `python api.py`，run起server，即可使用API查詢資料，API查詢範例為
	http://127.0.0.1:5000/get_data?area=3&lastname=&sex=boy&phone=&isowner=false
