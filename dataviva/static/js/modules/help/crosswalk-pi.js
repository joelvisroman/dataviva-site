var headers = {
    0: "hs_id",
    1: "cnae_id"
}

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var ProductsIndustryTable = function () {
    this.tableId = '#crosswalk-pi-table';

    this.table = $(this.tableId).DataTable({
        "ajax": {
            "url": "/help/crosswalk-pi/all",
            "dataSrc": "product_industry",
            "cache": true,
        },
        "order": [],
        "columns": [
            {
                render: function (data, type, row, meta){
                    return dataviva.hs[row[0]].name + ' (' + row[0] + ')';
                }
            },
            {
                render: function (data, type, row, meta){
                    if (dataviva.cnae[row[1]]){
                        return dataviva.cnae[row[1]].name + ' (' + row[1] + ')';
                    }
                    else{
                        return 'deu pau'
                    }

                }
            }
        ],
        "deferRender": true,
        "language": dataviva.datatables.language,
        "scrollY": 500,
        "scrollX": true,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

dataviva.requireAttrs(['hs', 'cnae'], function() {
    window.productIndustry = new ProductsIndustryTable(loadingRankings.hide);
});
