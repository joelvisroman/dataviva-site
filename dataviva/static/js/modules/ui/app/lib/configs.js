/* eslint quote-props:
  ["error", "as-needed", { "keywords": true, "unnecessary": false }] */

export function get_lang() {
  if (window.location.pathname.indexOf("pt") != -1) {
    return "pt";
  } else {
    return "en";
  }
}

export const env = {
  api_url: process.env.API_URL ?
    process.env.API_URL : "http://api.dataviva.info/",
  s3_host: process.env.S3_HOST ?
    process.env.S3_HOST : "https://dataviva-site-production.s3.amazonaws.com",
  lang: "pt",
};

export const databases = {
  location: {
    name: "message.brazilian_locations",
    code: "location",
    id_description: "message.id_ibge",
    group_opts: [
      "region",
      "state",
      "mesoregion",
      "microregion",
      "municipality",
    ],
    group_labels: [
      "region",
      "state",
      "mesoregion",
      "microregion",
      "municipality",
    ],
    order_opts: ["name", "extra_info"],
    order_labels: ["message.name", "message.population"],
    extra_info: {
      label: "Population",
    },
    endpoint: "municipality",
    img_path: {
      state: "/static/img/icons/bra/",
      mesoregion: "/static/img/icons/bra/",
      microregion: "/static/img/icons/bra/",
      municipality: "/static/img/icons/bra/",
    },
    icon: {
      db: "dv-bra",
      item: "dv-bra-",
    },
    tooltip_text: "message.brazilian_locations_tooltip",
    hidden_ids: [""],
    colors: {
      "1": "#00994c",
      "2": "#101070",
      "3": "#cfc417",
      "4": "#c40008",
      "5": "#90b72e",
    },
  },
  occupation: {
    name: "message.occupations",
    code: "occupation",
    id_description: "message.id_cbo",
    group_opts: ["occupation_group", "family"],
    group_labels: ["message.main_group", "message.family"],
    order_opts: ["name", "extra_info"],
    order_labels: ["message.name", "message.jobs"],
    extra_info: {
      label: "message.jobs",
      endpoint: "rais/occupation_family/?value=employee&year=2016&order=occupation_family",
      id: "occupation_family",
      data_value: "jobs",
    },
    endpoint: "occupation_family",
    icon: {
      db: "dv-occupation",
      item: "dv-cbo-",
    },
    tooltip_text: "message.occupations_tooltip",
    hidden_ids: ["0", "x"],
    colors: {
      "1": "#752277",
      "2": "#cc0000",
      "3": "#cf6117",
      "4": "#a47542",
      "5": "#17a3cf",
      "6": "#105b10",
      "7": "#31a0b5",
      "8": "#cf9f17",
      "9": "#581f05",
    },
    source: {
      database: "RAIS",
      year: "2016",
    },
  },
  industry: {
    name: "message.economic_activities",
    code: "industry",
    id_description: "message.id_cnae",
    group_opts: ["industry_section", "industry_division", "classe"],
    group_labels: ["message.section", "message.division", "message.class"],
    order_opts: ["name", "extra_info"],
    order_labels: ["message.name", "message.jobs"],
    extra_info: {
      label: "message.jobs",
      endpoint: "rais/industry_class/?value=employee&year=2016&order=industry_class",
      id: "industry_class",
      data_value: "jobs",
    },
    endpoint: "industry_class",
    icon: {
      db: "dv-industry",
      item: "dv-cnae-",
    },
    tooltip_text: "message.economic_activities_tooltip",
    hidden_ids: [""],
    colors: {
      a: "#105b10",
      b: "#330000",
      c: "#5e1f05",
      d: "#be2790",
      e: "#2f2f6d",
      f: "#cf7417",
      g: "#17a3cf",
      h: "#31a0b5",
      i: "#cf9f17",
      j: "#57d200",
      k: "#408e60",
      l: "#698b5a",
      m: "#cc0000",
      n: "#a47542",
      o: "#752277",
      p: "#cf6117",
      q: "#800000",
      r: "#7b6086",
      s: "#737373",
      t: "#cf1766",
      u: "#4c4c4c",
    },
    source: {
      database: "RAIS",
      year: "2016",
    },
  },
  product: {
    name: "message.products",
    code: "product",
    id_description: "message.id_hs",
    group_opts: ["product_section", "position"],
    group_labels: ["message.section", "message.position"],
    order_opts: ["name", "extra_info"],
    order_labels: ["message.name", "message.exports"],
    extra_info: {
      label: "message.exports",
      endpoint: "secex/product/?value=value&year=2017&order=product",
      id: "product",
      data_value: "value",
    },
    endpoint: "product",
    icon: {
      db: "dv-product",
      item: "dv-hs-",
    },
    tooltip_text: "message.products_tooltip",
    hidden_ids: ["22"],
    colors: {
      "01": "#cfa717",
      "02": "#cf9f17",
      "03": "#c87b1e",
      "04": "#adcf17",
      "05": "#330000",
      "06": "#be2790",
      "07": "#cf1766",
      "08": "#47b431",
      "09": "#b00000",
      "10": "#a47542",
      "11": "#105b10",
      "12": "#3ab11a",
      "13": "#cf6117",
      "14": "#752277",
      "15": "#5e1f05",
      "16": "#17a3cf",
      "17": "#31a0b5",
      "18": "#cf6117",
      "19": "#698b5a",
      "20": "#737373",
      "21": "#7b6086",
    },
    source: {
      database: "SECEX",
      year: "2017",
    },
  },
  trade_partner: {
    name: "message.trade_partners",
    code: "trade_partner",
    id_description: "message.id_wld",
    group_opts: ["continent", "country"],
    group_labels: ["message.continent", "message.country"],
    order_opts: ["name", "extra_info"],
    order_labels: ["message.name", "message.exports"],
    extra_info: {
      label: "message.exports",
      endpoint: "secex/country/?value=value&year=2017&order=country",
      id: "country",
      data_value: "value",
    },
    endpoint: "country",
    img_path: {
      country: "/static/img/icons/wld/",
    },
    icon: {
      db: "dv-trade-partner",
      item: "dv-wld-",
    },
    tooltip_text: "message.trade_partners_tooltip",
    hidden_ids: ["xx", "367"],
    colors: {
      as: "#c8140a",
      eu: "#752277",
      na: "#0b1097",
      sa: "#00923f",
      af: "#cf9f17",
      oc: "#cf7417",
    },
    source: {
      database: "SECEX",
      year: "2017",
    },
  },
  university: {
    name: "message.universities",
    code: "university",
    id_description: "message.id",
    order_opts: ["name", "extra_info"],
    order_labels: ["message.name", "message.enrolled"],
    extra_info: {
      label: "message.enrolled",
      endpoint: "hedu/university/?value=enrolled&year=2016&order=university",
      id: "university",
      data_value: "enrolleds",
    },
    endpoint: "university",
    icon: {
      db: "dv-university",
      item: "dv-university-",
    },
    tooltip_text: "message.universities_tooltip",
    hidden_ids: ["x"],
    colors: {
      T: "#31a0b5",
      S: "#2f2f6d",
      Q: "#009b3a",
      P: "#105b10",
    },
    source: {
      database: "Censo da Educação Superior",
      year: "2016",
    },
  },
  hedu_course: {
    name: "message.higher_education",
    code: "hedu_course",
    id_description: "message.id",
    group_opts: ["hedu_course_field", "major"],
    group_labels: ["message.field", "message.major"],
    order_opts: ["name", "extra_info"],
    order_labels: ["message.name", "message.enrolled"],
    extra_info: {
      label: "message.enrolled",
      endpoint: "hedu/hedu_course/?value=enrolled&year=2016&order=hedu_course",
      id: "hedu_course",
      data_value: "enrolleds",
    },
    endpoint: "hedu_course",
    icon: {
      db: "dv-major",
      item: "dv-course-hedu-",
    },
    tooltip_text: "message.higher_education_tooltip",
    hidden_ids: ["00"],
    colors: {
      "01": "#737373",
      "14": "#cc0000",
      "21": "#7b6086",
      "22": "#cf6117",
      "31": "#c87b1e",
      "32": "#57d200",
      "34": "#a47542",
      "38": "#752277",
      "42": "#cf1766",
      "44": "#be2790",
      "46": "#408e60",
      "48": "#23c2b7",
      "52": "#17a3cf",
      "54": "#581f05",
      "58": "#cf7417",
      "62": "#105B10",
      "64": "#47b431",
      "72": "#800000",
      "76": "#cfa717",
      "81": "#cf9f17",
      "84": "#31a0b5",
      "85": "#2f2f6d",
      "86": "#698b5a",
    },
    source: {
      database: "Censo da Educação Superior",
      year: "2016",
    },
  },
  basic_course: {
    name: "message.basic_courses",
    code: "basic_course",
    id_description: "message.id",
    group_opts: ["course_field", "course"],
    group_labels: ["message.field", "message.course"],
    order_opts: ["name", "extra_info"],
    order_labels: ["message.name", "message.enrolled"],
    extra_info: {
      label: "message.enrolled",
      endpoint: "sc/sc_course/?value=students&year=2017&order=sc_course",
      id: "sc_course",
      data_value: "students",
    },
    endpoint: "sc_course",
    icon: {
      db: "dv-basic-course",
      item: "dv-course-sc-",
    },
    tooltip_text: "message.basic_courses_tooltip",
    hidden_ids: ["00"],
    colors: {
      "XX": "#2f2f6d",
      "01": "#800000",
      "02": "#CC0000",
      "03": "#17a3cf",
      "04": "#a47542",
      "05": "#cf9f17",
      "06": "#57d200",
      "07": "#31a0b5",
      "08": "#698b5a",
      "09": "#c87b1e",
      "10": "#7b6086",
      "11": "#581f05",
      "12": "#105b10",
      "13": "#cf7417",
    },
    source: {
      database: "Censo Escolar",
      year: "2017",
    },
  },
};
