from mutool.reader import *
from mutool.writer import *
from mutool.constants import *
from mutool.date import *
from bs4 import BeautifulSoup
import re,json
import configparser #引入模块

req = requests.session()
req.headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'x-ab-param':'se_expired_ob=0;se_backsearch=0;tp_topic_tab_new=0-0-0;tp_movie_ux=2;se_cardrank_3=0;li_topics_search=0;li_video_section=1;se_bert_eng=0;se_searchwiki=0;zw_sameq_sorce=999;se_content0=1;zr_test_aa1=0;tp_club_top=0;ug_newtag=1;zr_ans_rec=gbrank;li_svip_cardshow=1;se_searchvideo=3;tp_club_bt=0;ls_recommend_test=5;se_video_v2=0;pf_profile2_tab=0;zr_training_boost=false;tp_club_feed=0;tp_dingyue_video=0;tp_move_scorecard=0;tp_club_feedv3=0;se_billboardsearch=0;zr_search_topic=0;se_clarify=1;se_v049=0;tp_club_qa_entrance=1;pf_adjust=1;qap_question_author=0;zr_search_sim2=0;se_click_v_v=0;se_hlt_trunc=0;se_v048=0;tp_club_fdv4=0;tsp_ad_cardredesign=0;pf_noti_entry_num=1;soc_feed_intelligent=0;li_se_section=1;se_college=default;soc_adweeklynew=2;soc_iosweeklynew=2;li_svip_tab_search=1;qap_question_visitor= 0;zr_rec_answer_cp=open;se_v045=0;tp_club_new=0;ls_videoad=2;li_salt_hot=1;li_ebook_gen_search=2;se_adsrank=4;se_v040_2=2;tp_club__entrance2=1;tp_topic_entry=0;tp_m_intro_re_topic=1;li_car_meta=0;zr_search_sims=0;se_colorfultab=1;tp_club_entrance=1;top_universalebook=1;top_test_4_liguangyi=1;zr_art_rec=base;tp_score_1=a;tsp_hotlist_ui=3;ls_fmp4=0;tp_topic_style=0;top_hotcommerce=1;zr_km_answer=open_cvr;zr_expslotpaid=1;se_whitelist=1;li_vip_verti_search=0;zr_rel_search=base;se_web0answer=0;se_aa_base=1;tp_club_reactionv2=0;ls_video_commercial=0;se_v040=0;se_topic_wei=0;li_panswer_topic=1;zr_zr_search_sims=0;zr_intervene=0;zr_slotpaidexp=8;tp_discover=1;ug_follow_topic_1=2;qap_labeltype=1;se_ffzx_jushen1=0;se_video_tab=1;se_mobilecard=0;se_v046=0;tp_meta_card=0;tp_club_flow_ai=1;se_wil_act=0;zr_training_first=true;se_col_boost=1;pf_fuceng=1;pf_foltopic_usernum=50;li_viptab_name=0;se_sug_term=0;tp_topic_tab=0;tp_header_style=1;tsp_ios_cardredesign=0;se_topicfeed=0;se_new_bert=0;se_entity22=1;se_oneboxtopic=1;se_v044=0;se_bsi=0;tp_sft=a;zr_search_paid=1;pf_creator_card=1;li_training_chapter=1;se_v043=0;soc_notification=1;top_ebook=0;li_paid_answer_exp=0;top_v_album=1;top_root=0;pf_newguide_vertical=0;li_answer_card=0;li_yxzl_new_style_a=1;zr_slot_training=2;se_multi_images=0;se_videobox=0;top_quality=0;ug_goodcomment_0=1;li_catalog_card=1',
    'x-api-version':'3.0.40',
    'x-requested-with':'fetch',
    'x-zse-83':'3_2.0',
    'x-zse-86':'1.0_a8O8FgH86HFpcTt0Y_O8oHXqoHFXgCSqYLYy2098nq2Y',
    'x-zst-81':'3_2.0ae3TnRUTEvOOUCNMTQnTSHUZo02p-HNMZBO8YD7qQXtu2RY0K6P0EHuy-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_Ie8FL7AtqM6O1VDQyQ6nxrRPCHukMoCXBEgOsiRP0XL2ZUBXmDDV9qhnyTXFMnXcTF_ntRueThio1beu96qeMJhXCqCxKQvLmoqgsoTOYjqV0Hro8nBwpIB29mDoCUboC27LPvMo8RwVqeUo_bLXBFCg0yCg_YJLmUwSmOwYmY8wmIgg8-Bes2CXLhUofQDpG-DcsOhS0sCcCXBS8cwFx_UVB0BV1r7HfUuwsNw38nuwqoQLyECc1VGV0vqfzoD9fovL1bUwY-gFK0ucVCBx80Ue_wCXqLv9_yUSukgVyp4NK8UgOXuc8CqOBvGOYHc3K0gSxWcOyFhwBfuOB9wLVriN8pwwMTJCBc4HxrC3YuweL3JrC',
}

req.headers['Cookie'] = 'SESSIONID=0UV2HhvH0L76Kg4fARWjahChMbTdvvwQBr2Fx4AR7tU; JOID=UFgdBEkuKvXTwBs8XyuIbNhepktEDwHZ9eM6F3MNC97_5jgddE9tEIjCETtV4_weFdFwIJY4t5pKT8nDWvpLwFM=; osd=VlEWA0woI_7UxR01VCyNatFVoU5CBgre8OUzHHQIDdf04T0bfURqFY7LGjxQ5fUVEtR2KZ0_spxDRM7GXPNAx1Y=; _zap=a4deda8d-08cc-4a92-bda6-00a06bed46c6; _xsrf=12sTRHwEkG0zG1PLMDF8cnzsEt24TAls; d_c0="AACnB-0fKBCPToeAGH-TrMfYNQiOUk0uQzI=|1570350630"; __utma=51854390.1394818494.1585912119.1585912119.1585912119.1; __utmz=51854390.1585912119.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.000--|3=entry_date=20200228=1; z_c0=Mi4xblFLQUJ3QUFBQUFBQUtjSDdSOG9FQmNBQUFCaEFsVk5ITEIxWHdCRUJLVC1ISHBOV3A5amVhTS1iVGxKVENGOThB|1585996316|5ba7f09d48d4b11c63f7d86cc45cb281fd2ef831; tst=r; q_c1=b2033236d0e24f9aa59ad12f413dd396|1592130773000|1592130773000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1592130773,1592130830,1592660395,1592735608; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1592737909; KLBRSID=cdfcc1d45d024a211bb7144f66bda2cf|1592737940|1592735606'
def resetIp():
    global req
    req = requests.session()
    url = "http://api.wandoudl.com/api/ip?app_key=e6c05c9a4209e893f38c63b22e979316&pack=207335&num=1&xy=3&type=1&lb=\n&mr=1&"
    txt = requests.get(url).content.decode("utf-8")

    # req.headers['Proxy-Connection'] = 'keep-alive'
    req.proxies = {
        'http': 'socks5://{}'.format(txt.replace("\n", "").strip()),
        'https': 'socks5://{}'.format(txt.replace("\n", "").strip())
    }
    print(req.proxies)


def userIndex(user,qid):
    global req
    url = "https://www.zhihu.com/question/{}".format(qid)
    html, req, status = getSource(url, session=req)
    reg = re.compile('<meta itemProp="url" content="https://www\.zhihu\.com/people/(.*?)"/>').findall(html)
    if len(reg) >= 2:
        num = 0
        for item in reg:
            if num == 2:
                return
            if item:
                num += 1
                dataItem = [user,qid,item]
                print(dataItem)
                writerToCsv("extendUser.csv",[dataItem])
def func(user,qid):
    userIndex(user,qid)

def main():
    source = csvReader("extendSource.csv")
    for user,qids in source:
        qids = qids.strip('[]').split(', ')[-10:]
        for qid in qids:
            if qid:
                func(user,qid)
if __name__ == '__main__':
    main()
