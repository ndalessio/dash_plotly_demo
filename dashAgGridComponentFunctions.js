var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};


dagcomponentfuncs.DeleteButton = function (props) {
    function onClick() {
          props.api.applyTransaction({ remove: [props.node.data] })
    }
    return React.createElement('button', {onClick}, "X");
};
