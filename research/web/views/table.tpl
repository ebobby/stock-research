% scroll = scroll if "scroll" in vars() else True

% if len(rows) == 0 or not rows[0]:
  No data
% else:
<div class="{{'table-responsive' if scroll else ''}}">
  <table class="table table-striped">
    <thead>
      <tr>
         <th>#</th>
%   for col in list(rows[0].keys()):
%     if col == 'logo_url':
         <th scope="col">Logo</th>
%     elif col in ['date', 'last_date', 'price_date']:
         <th scope="col" style="min-width: 100px">{{' '.join(w.capitalize() for w in col.split('_'))}}</th>
%     elif col in ['company', 'industry', 'sector', 'company_name']:
         <th scope="col" style="min-width: 200px">{{' '.join(w.capitalize() for w in col.split('_'))}}</th>
%     else:
         <th scope="col" style="overflow:hidden; white-space: nowrap;">{{' '.join(w.capitalize() for w in col.split('_'))}}</th>
%     end
%   end
      </tr>
    </thead>
    <tbody>
%   for i, row in enumerate(rows):
      <tr>
        <th scope="row">{{i+1}}</th>
%     for key in row.keys():
%       if key == 'symbol':
          <td><a href="/stock/{{row[key]}}" target="_blank">{{row[key]}}</a></td>
%       elif key == 'url':
          <td><a href="{{row[key]}}" target="_blank">website</a></td>
%       elif key in ['company', 'industry', 'sector', 'company_name']:
          <td style="overflow:hidden; white-space: nowrap;">{{row[key]}}</td>
%       elif key == 'logo_url':
          <td style="text-align: center;vertical-align:middle;width:100%"><img class="img-fluid img-thumbnail" src="{{row[key]}}" style="max-width:35px;" /></td>
%       elif key == 'yahoo_url':
          <td><a href="{{row[key]}}" target="_blank">yahoo</a></td>
%       elif key in ['return_on_investment', 'annual_return', 'rate_of_return', 'cagr', 'return_on_retained_earnings', 'earnings_growth', 'validation_cagr', 'estimated_rate_of_return', 'margin', 'discount_rate']:
%         if row[key]:
              <td>{{f"{round(float(row[key]) * 100.0, 2)}%"}}</td>
%         else:
              <td>N/A</td>
%         end
%       elif key in ['open', 'close', 'high', 'low', 'eps', 'eps_1y', 'eps_5y', 'eps_10y', 'share_price', 'estimated_eps', 'estimated_price', 'dcf_price', 'discounted_cash_flows', 'discounted_share_price']:
%         if row[key]:
              <td>{{"${:,.2f}".format(row[key])}}</td>
%         else:
              <td>N/A</td>
%         end
%       else:
         <td title="{{key}}">{{row[key]}}</td>
%       end
%     end
      </tr>
%   end
    </tbodY>
  </table>
</div>
% end
