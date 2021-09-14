% if len(rows) == 0 or not rows[0]:
  No data
% else:
  <table class="table table-striped table-hover table-scroll">
    <thead>
      <tr>
         <th>#</th>
%   for col in list(rows[0].keys()):
         <th style="min-width: 120px">{{' '.join(w.capitalize() for w in col.split('_'))}}</th>
%   end
      </tr>
    </thead>
    <tbody>
%   for i, row in enumerate(rows):
      <tr>
        <td>{{i+1}}</td>
%     for key in row.keys():
%       if key == 'symbol':
          <td><a href="/stock/{{row[key]}}" target="_blank">{{row[key]}}</a></td>
%       elif key == 'url':
          <td><a href="{{row[key]}}" target="_blank">website</a></td>
%       elif key == 'yahoo_url':
          <td><a href="{{row[key]}}" target="_blank">yahoo</a></td>
%       elif key in ['return_on_investment', 'annual_return', 'rate_of_return', 'cagr', 'return_on_retained_earnings', 'earnings_growth', 'validation_cagr', 'estimated_rate_of_return', 'margin']:
%         if row[key]:
              <td>{{f"{round(float(row[key]) * 100.0, 2)}%"}}</td>
%         else:
              <td>N/A</td>
%         end
%       elif key in ['open', 'close', 'high', 'low', 'eps', 'eps_1y', 'eps_5y', 'eps_10y', 'share_price', 'estimated_eps', 'estimated_price', 'dcf_price']:
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
% end
