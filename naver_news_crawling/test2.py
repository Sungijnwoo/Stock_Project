

    # ######### 언론사 선택 및 confirm #####################
    # print('설정한 언론사를 선택합니다.\n')
    # search_opt_box = browser.find_element_by_xpath('//*[@id="search_option_button"]')
    # search_opt_box.click()
    # time.sleep(0.02)

    # # 언론사 선택하는 바를 활성화
    # tablist_box = browser.find_element_by_xpath('//div[@class="snb_inner"]/ul[@role="tablist" and @class="option_menu"]')

    # tablist_elem_list = tablist_box.find_elements_by_xpath('./li[@role="presentation"]')
    # press_box = [t for t in tablist_elem_list if t.text == '언론사'][0].find_element_by_xpath('./a')
    # press_box.click()


    # # 언론사 종류 하나씩 선택
    # actived_press_frame = browser.find_element_by_xpath('.//div[@class="snb_itembox lst_press _search_option_press_"]')
    # total_press_box = actived_press_frame.find_element_by_xpath('./div[@class="group_sort type_press _group_by_press_"]')

    # # 언론사 종류를 선택하는 버튼이 담긴 박스
    # press_cat_active_button = total_press_box.find_elements_by_xpath('.//a[@role="tab" and @class="item _tab_filter_"]') # 언론사 종류 하나씩 버튼
    # press_cat_active_button_dict = dict(zip([t.text for t in press_cat_active_button], press_cat_active_button)) # 언론사 종류 이름 : 언론사 종류 활성화 버튼

    # # 밑에 각 언론사 종류별 개별 언론사가 담겨있는 박스들
    # each_press_box_list = total_press_box.find_elements_by_xpath('.//div[@class="scroll_area _panel_filter_"]')

    # # 1. 언론사 종류 1개 선택
    # # 2. 선택한 언론사 종류에 해당하는 개별 언론사 중 크롤링할 언론사에 포함되는 것 체크 
    # for idx, press_cat_name in enumerate(press_cat_active_button_dict.keys()):
    #     #하나의 언론사 종류를 클릭해서 활성화시킴
    #     press_cat_active_button_dict[press_cat_name].click()
    #     time.sleep(0.05)
        
    #     # 선택한 언론사 종류 안의 개별 언론사가 담긴 박스
    #     each_press_box = each_press_box_list[idx].find_element_by_xpath('./div[@class="select_item"]')
    #     # 개별 언론사의 이름
    #     each_press_title_list = [ep.get_attribute('title') for ep in each_press_box.find_elements_by_xpath('.//label')]
    #     # 개별 언론사 체크 박스
    #     each_press_input_list = each_press_box.find_elements_by_xpath('.//input')
        

    #     # 딕셔너리(개별 언론사 이름 : 개별 언론사 체크 박스)
    #     each_press_title_input_dict = dict(zip(each_press_title_list, each_press_input_list))
    #     # 추출하고 싶은 언론사 존재 시 체크박스 클릭
    #     for title in [tit for tit in each_press_title_input_dict.keys() if tit in press_list]:
    #         print(title)
    #         each_press_title_input_dict[title].click()


    # # 확인 버튼
    # confirm_buttons = actived_press_frame.find_element_by_xpath('./span[@class="btn_inp"]').find_elements_by_xpath('.//button')
    # ok_button = [c for c in confirm_buttons if c.text == '확인'][0]
    # ok_button.click()
